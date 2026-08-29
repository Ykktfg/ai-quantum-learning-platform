from fastapi.testclient import TestClient

from app.main import app
from app.db.models import User, Course, Enrollment
from app.auth.security import hash_password

from tests.conftest import TestingSessionLocal


# ============================================================
# TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# CONSTANTS
# ============================================================

TEST_EMAIL = "course-test@example.com"
TEST_PASSWORD = "TestPassword123"
TEST_COURSE_TITLE = "Quantum Fundamentals Test"


# ============================================================
# TEST USER
# ============================================================

def create_test_user():
    """
    Create the course test user if it does not exist.

    If the user already exists, reset the password and
    other fields so authentication is always predictable.
    """

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == TEST_EMAIL)
            .first()
        )

        if user is None:

            user = User(
                email=TEST_EMAIL,
                name="Course Test Student",
                role="student",
                password_hash=hash_password(
                    TEST_PASSWORD
                ),
            )

            db.add(user)

        else:

            user.name = "Course Test Student"
            user.role = "student"

            # IMPORTANT:
            # Always reset the password because the same
            # SQLite test database is shared between tests.
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
    Create the test course if it does not exist.
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
                    "A test course for quantum computing."
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
# AUTH TOKEN
# ============================================================

def get_auth_token():
    """
    Create/reset the test user and obtain a valid JWT.
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
# GET ALL COURSES
# ============================================================

def test_get_all_courses():

    course_id = create_test_course()

    response = client.get(
        "/api/courses"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "courses" in data

    assert data["count"] >= 1

    course_ids = [
        course["id"]
        for course in data["courses"]
    ]

    assert course_id in course_ids


# ============================================================
# GET COURSE BY ID
# ============================================================

def test_get_course_by_id():

    course_id = create_test_course()

    response = client.get(
        f"/api/courses/{course_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == course_id
    assert data["title"] == TEST_COURSE_TITLE
    assert data["level"] == "beginner"


# ============================================================
# GET NONEXISTENT COURSE
# ============================================================

def test_get_nonexistent_course():

    response = client.get(
        "/api/courses/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Course not found"


# ============================================================
# ENROLL IN COURSE
# ============================================================

def test_enroll_in_course():

    user_id = create_test_user()
    token = get_auth_token()
    course_id = create_test_course()

    # --------------------------------------------------------
    # Remove previous enrollment
    # --------------------------------------------------------

    db = TestingSessionLocal()

    try:

        existing = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if existing:

            db.delete(existing)
            db.commit()

    finally:
        db.close()

    # --------------------------------------------------------
    # Enroll
    # --------------------------------------------------------

    response = client.post(
        "/api/enrollments",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["course_id"] == course_id
    assert data["status"] == "active"


# ============================================================
# GET MY ENROLLMENTS
# ============================================================

def test_get_my_enrollments():

    user_id = create_test_user()
    token = get_auth_token()
    course_id = create_test_course()

    # --------------------------------------------------------
    # Make sure the user is enrolled
    # --------------------------------------------------------

    db = TestingSessionLocal()

    try:

        existing = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if existing is None:

            enrollment = Enrollment(
                user_id=user_id,
                course_id=course_id,
                status="active",
            )

            db.add(enrollment)
            db.commit()

    finally:
        db.close()

    # --------------------------------------------------------
    # Get enrollments
    # --------------------------------------------------------

    response = client.get(
        "/api/enrollments/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    course_ids = [
        enrollment["course_id"]
        for enrollment in data
    ]

    assert course_id in course_ids


# ============================================================
# DUPLICATE ENROLLMENT
# ============================================================

def test_duplicate_enrollment():

    user_id = create_test_user()
    token = get_auth_token()
    course_id = create_test_course()

    # --------------------------------------------------------
    # Clean previous enrollment
    # --------------------------------------------------------

    db = TestingSessionLocal()

    try:

        existing = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if existing:

            db.delete(existing)
            db.commit()

    finally:
        db.close()

    # --------------------------------------------------------
    # First enrollment
    # --------------------------------------------------------

    first_response = client.post(
        "/api/enrollments",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id
        },
    )

    assert first_response.status_code == 200, (
        first_response.text
    )

    # --------------------------------------------------------
    # Second enrollment
    # --------------------------------------------------------

    second_response = client.post(
        "/api/enrollments",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": course_id
        },
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert (
        data["detail"]
        == "User is already enrolled in this course"
    )


# ============================================================
# ENROLL IN NONEXISTENT COURSE
# ============================================================

def test_enroll_nonexistent_course():

    token = get_auth_token()

    response = client.post(
        "/api/enrollments",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_id": 999999
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Course not found"


# ============================================================
# ENROLLMENT WITHOUT AUTHENTICATION
# ============================================================

def test_enrollment_without_token():

    course_id = create_test_course()

    response = client.post(
        "/api/enrollments",
        json={
            "course_id": course_id
        },
    )

    assert response.status_code == 401