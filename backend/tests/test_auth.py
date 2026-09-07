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
# TEST CONSTANTS
# ============================================================

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "TestPassword123"
TEST_NAME = "Test Student"
TEST_ROLE = "student"


# ============================================================
# CREATE / RESET TEST USER
# ============================================================

def create_test_user():
    """
    Create the authentication test user.

    If the user already exists, reset all important fields,
    especially the password, so every test starts with the
    same known credentials.
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

        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        if user is None:

            user = User(
                email=TEST_EMAIL,
                name=TEST_NAME,
                role=TEST_ROLE,
                password_hash=hash_password(
                    TEST_PASSWORD
                ),
            )

            db.add(user)

        # ----------------------------------------------------
        # RESET EXISTING USER
        # ----------------------------------------------------

        else:

            user.email = TEST_EMAIL
            user.name = TEST_NAME
            user.role = TEST_ROLE

            # IMPORTANT:
            # Always reset password.
            user.password_hash = hash_password(
                TEST_PASSWORD
            )

        db.commit()
        db.refresh(user)

        return user.id

    finally:

        db.close()


# ============================================================
# LOGIN HELPER
# ============================================================

def login_test_user():
    """
    Create/reset the test user and log in.

    Returns:
        access_token
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
# LOGIN SUCCESS
# ============================================================

def test_login_success():

    create_test_user()

    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    # Debug information
    print("\n========================================")
    print("LOGIN STATUS:", response.status_code)
    print("LOGIN RESPONSE:", response.json())
    print("========================================\n")

    assert response.status_code == 200

    data = response.json()

    # --------------------------------------------------------
    # TOKEN
    # --------------------------------------------------------

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    assert "user" in data

    assert data["user"]["email"] == TEST_EMAIL
    assert data["user"]["name"] == TEST_NAME
    assert data["user"]["role"] == TEST_ROLE


# ============================================================
# INVALID PASSWORD
# ============================================================

def test_login_invalid_password():

    create_test_user()

    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


# ============================================================
# INVALID EMAIL
# ============================================================

def test_login_invalid_email():

    response = client.post(
        "/api/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


# ============================================================
# PROTECTED ENDPOINT WITHOUT TOKEN
# ============================================================

def test_protected_endpoint_without_token():

    response = client.get(
        "/api/users/me"
    )

    assert response.status_code == 401


# ============================================================
# PROTECTED ENDPOINT WITH VALID TOKEN
# ============================================================

def test_protected_endpoint_with_valid_token():

    token = login_test_user()

    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Debug information
    print("\n========================================")
    print("ME STATUS:", response.status_code)
    print("ME RESPONSE:", response.json())
    print("========================================\n")

    assert response.status_code == 200

    data = response.json()

    # --------------------------------------------------------
    # RESPONSE STRUCTURE
    # --------------------------------------------------------

    assert data["success"] is True

    # --------------------------------------------------------
    # USER DATA
    # --------------------------------------------------------

    assert data["user"]["email"] == TEST_EMAIL
    assert data["user"]["name"] == TEST_NAME
    assert data["user"]["role"] == TEST_ROLE


# ============================================================
# PROTECTED ENDPOINT WITH INVALID TOKEN
# ============================================================

def test_protected_endpoint_with_invalid_token():

    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401