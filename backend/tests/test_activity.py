from fastapi.testclient import TestClient

from app.main import app
from app.db.models import User
from app.auth.security import hash_password

from tests.conftest import TestingSessionLocal


# ============================================================
# TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# CONSTANTS
# ============================================================

TEST_EMAIL = "activity-test@example.com"
TEST_PASSWORD = "TestPassword123"


# ============================================================
# TEST USER
# ============================================================

def create_test_user(
    email=TEST_EMAIL,
    name="Activity Test Student",
):
    """
    Create or reset a test user.
    """

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            user = User(
                email=email,
                name=name,
                role="student",
                password_hash=hash_password(
                    TEST_PASSWORD
                ),
            )

            db.add(user)

        else:
            user.name = name
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
# AUTH TOKEN
# ============================================================

def get_auth_token(
    email=TEST_EMAIL,
):
    """
    Create/reset user and obtain JWT.
    """

    create_test_user(email=email)

    response = client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert "access_token" in data

    return data["access_token"]


# ============================================================
# ACTIVITY PAYLOAD
# ============================================================

def activity_payload(
    activity_type="lesson_completed",
    course_id=1,
    description="Completed introduction to quantum computing",
):
    return {
        "activity_type": activity_type,
        "course_id": course_id,
        "description": description,
    }


# ============================================================
# CREATE ACTIVITY
# ============================================================

def test_create_activity():

    token = get_auth_token()

    response = client.post(
        "/api/activity",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=activity_payload(),
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] > 0
    assert data["user_id"] > 0
    assert data["activity_type"] == "lesson_completed"
    assert data["course_id"] == 1
    assert (
        data["description"]
        == "Completed introduction to quantum computing"
    )


# ============================================================
# CREATE ACTIVITY WITHOUT TOKEN
# ============================================================

def test_create_activity_without_token():

    response = client.post(
        "/api/activity",
        json=activity_payload(),
    )

    assert response.status_code == 401


# ============================================================
# GET MY ACTIVITIES
# ============================================================

def test_get_my_activities():

    token = get_auth_token()

    create_response = client.post(
        "/api/activity",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=activity_payload(
            activity_type="quiz_completed",
            description="Completed quantum quiz",
        ),
    )

    assert create_response.status_code == 200

    response = client.get(
        "/api/activity/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    activity_types = [
        activity["activity_type"]
        for activity in data
    ]

    assert "quiz_completed" in activity_types


# ============================================================
# GET MY ACTIVITIES WITHOUT TOKEN
# ============================================================

def test_get_my_activities_without_token():

    response = client.get(
        "/api/activity/me"
    )

    assert response.status_code == 401


# ============================================================
# USER ISOLATION
# ============================================================

def test_activity_user_isolation():

    token1 = get_auth_token(
        "activity-owner@example.com"
    )

    create_response = client.post(
        "/api/activity",
        headers={
            "Authorization": f"Bearer {token1}"
        },
        json=activity_payload(
            activity_type="private_activity",
            description="Private user activity",
        ),
    )

    assert create_response.status_code == 200

    token2 = get_auth_token(
        "different-activity-user@example.com"
    )

    response = client.get(
        "/api/activity/me",
        headers={
            "Authorization": f"Bearer {token2}"
        },
    )

    assert response.status_code == 200

    activities = response.json()

    for activity in activities:
        assert activity["description"] != (
            "Private user activity"
        )


# ============================================================
# ACTIVITY WITHOUT COURSE
# ============================================================

def test_create_activity_without_course():

    token = get_auth_token()

    response = client.post(
        "/api/activity",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "activity_type": "login",
            "course_id": None,
            "description": "Student logged into platform",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["activity_type"] == "login"
    assert data["course_id"] is None
    assert (
        data["description"]
        == "Student logged into platform"
    )