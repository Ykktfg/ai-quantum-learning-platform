from fastapi.testclient import TestClient

from app.main import app
from app.db.models import (
    User,
    Course,
    Enrollment,
    Progress,
)
from app.auth.security import hash_password

from tests.conftest import TestingSessionLocal


# ============================================================
# TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# CONSTANTS
# ============================================================

TEST_EMAIL = "progress-test@example.com"
TEST_PASSWORD = "TestPassword123"
TEST_COURSE_TITLE = "Progress Test Quantum Course"


# ============================================================
# TEST USER
# ============================================================

def create_test_user():
    """
    Create or reset the progress test user.
    """

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(
                User.email == TEST_EMAIL
            )
            .first()
        )

        if user is None:

            user = User(
                email=TEST_EMAIL,
                name="Progress Test Student",
                role="student",
                password_hash=hash_password(
                    TEST_PASSWORD
                ),
            )

            db.add(user)

        else:

            user.name = "Progress Test Student"
            user.role = "student"
            user.password_hash = hash_password(
                TEST_PASSWORD
            )

        db.commit()
        db.refresh(user)

        return user.id

    finally:
        db.close()


# ============================================================
# TEST COURSE
# ============================================================

def create_test_course():
    """
    Create the progress test course if it does not exist.
    """

    db = TestingSessionLocal()

    try:
        course = (
            db.query(Course)
            .filter(
                Course.title == TEST_COURSE_TITLE
            )
            .first()
        )

        if course is None:

            course = Course(
                title=TEST_COURSE_TITLE,
                description=(
                    "A test course for progress tracking."
                ),
                level="beginner",
                duration="4 weeks",
                category="quantum-computing",
            )

            db.add(course)
            db.commit()
            db.refresh(course)

        return course.id

    finally:
        db.close()


# ============================================================
# ENROLL TEST USER
# ============================================================

def enroll_test_user(course_id):
    """
    Enroll the progress test user in a course.
    """

    user_id = create_test_user()

    db = TestingSessionLocal()

    try:

        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if enrollment is None:

            enrollment = Enrollment(
                user_id=user_id,
                course_id=course_id,
                status="active",
            )

            db.add(enrollment)

        else:

            enrollment.status = "active"

        db.commit()

    finally:
        db.close()


# ============================================================
# GET AUTH TOKEN
# ============================================================

def get_auth_token():
    """
    Create/reset user and obtain a JWT token.
    """

    create_test_user()

    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200, (
        f"Login failed: {response.text}"
    )

    data = response.json()

    assert "access_token" in data

    return data["access_token"]


# ============================================================
# CLEANUP PROGRESS
# ============================================================

def cleanup_progress(course_id):
    """
    Remove existing progress for the test user/course.
    """

    user_id = create_test_user()

    db = TestingSessionLocal()

    try:

        existing = (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
                Progress.course_id == course_id,
            )
            .first()
        )

        if existing:
            db.delete(existing)
            db.commit()

    finally:
        db.close()


# ============================================================
# UPDATE PROGRESS WITHOUT AUTHENTICATION
# ============================================================

def test_update_progress_without_token():

    course_id = create_test_course()

    response = client.post(
        "/api/progress",
        json={
            "course_id": course_id,
            "completion_percentage": 25,
            "completed_lessons": 1,
        },
    )

    assert response.status_code == 401


# ============================================================
# UPDATE PROGRESS FOR NONEXISTENT COURSE
# ============================================================

def test_update_progress_nonexistent_course():

    token = get_auth_token()

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": 999999,
            "completion_percentage": 25,
            "completed_lessons": 1,
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Course not found"


# ============================================================
# UPDATE PROGRESS WITHOUT ENROLLMENT
# ============================================================

def test_update_progress_without_enrollment():

    token = get_auth_token()
    course_id = create_test_course()

    cleanup_progress(course_id)

    user_id = create_test_user()

    db = TestingSessionLocal()

    try:

        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if enrollment:
            db.delete(enrollment)
            db.commit()

    finally:
        db.close()

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 25,
            "completed_lessons": 1,
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert (
        data["detail"]
        == "You must be enrolled in this course to update progress"
    )


# ============================================================
# CREATE PROGRESS - NOT STARTED
# ============================================================

def test_create_progress_not_started():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)
    cleanup_progress(course_id)

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 0,
            "completed_lessons": 0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_id"] == course_id
    assert data["completion_percentage"] == 0
    assert data["completed_lessons"] == 0
    assert data["status"] == "not_started"


# ============================================================
# UPDATE PROGRESS - IN PROGRESS
# ============================================================

def test_update_progress_in_progress():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 50,
            "completed_lessons": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_id"] == course_id
    assert data["completion_percentage"] == 50
    assert data["completed_lessons"] == 2
    assert data["status"] == "in_progress"


# ============================================================
# UPDATE PROGRESS - COMPLETED
# ============================================================

def test_update_progress_completed():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 100,
            "completed_lessons": 4,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_id"] == course_id
    assert data["completion_percentage"] == 100
    assert data["completed_lessons"] == 4
    assert data["status"] == "completed"


# ============================================================
# GET MY PROGRESS
# ============================================================

def test_get_my_progress():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)
    cleanup_progress(course_id)

    create_response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 50,
            "completed_lessons": 2,
        },
    )

    assert create_response.status_code == 200

    response = client.get(
        "/api/progress/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    course_ids = [
        progress["course_id"]
        for progress in data
    ]

    assert course_id in course_ids


# ============================================================
# GET PROGRESS FOR ONE COURSE
# ============================================================

def test_get_course_progress():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)
    cleanup_progress(course_id)

    create_response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 75,
            "completed_lessons": 3,
        },
    )

    assert create_response.status_code == 200

    response = client.get(
        f"/api/progress/{course_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_id"] == course_id
    assert data["completion_percentage"] == 75
    assert data["completed_lessons"] == 3
    assert data["status"] == "in_progress"


# ============================================================
# GET PROGRESS FOR COURSE WITH NO PROGRESS
# ============================================================

def test_get_course_progress_not_found():

    token = get_auth_token()

    db = TestingSessionLocal()

    try:

        course = Course(
            title="No Progress Course",
            description=(
                "A course without a progress record."
            ),
            level="beginner",
            duration="2 weeks",
            category="quantum-computing",
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        course_id = course.id

    finally:
        db.close()

    response = client.get(
        f"/api/progress/{course_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert (
        data["detail"]
        == "Progress not found for this course"
    )


# ============================================================
# INVALID PROGRESS VALUE
# ============================================================

def test_invalid_progress_percentage():

    token = get_auth_token()
    course_id = create_test_course()

    enroll_test_user(course_id)

    response = client.post(
        "/api/progress",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id,
            "completion_percentage": 150,
            "completed_lessons": 5,
        },
    )

    assert response.status_code == 422