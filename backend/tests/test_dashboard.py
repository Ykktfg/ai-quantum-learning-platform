from fastapi.testclient import TestClient

from app.main import app
from app.db.models import (
    User,
    Course,
    Enrollment,
    Progress,
    Circuit,
    Simulation,
)
from app.auth.security import hash_password

from tests.conftest import TestingSessionLocal


client = TestClient(app)


# ============================================================
# CONSTANTS
# ============================================================

TEST_EMAIL = "dashboard-test@example.com"
TEST_PASSWORD = "TestPassword123"


# ============================================================
# CREATE TEST USER
# ============================================================

def create_test_user(
    email=TEST_EMAIL,
    name="Dashboard Test Student",
):
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
# GET AUTH TOKEN
# ============================================================

def get_auth_token(
    email=TEST_EMAIL,
):
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
# TEST 1 - DASHBOARD WITHOUT TOKEN
# ============================================================

def test_dashboard_without_token():

    response = client.get(
        "/api/dashboard"
    )

    assert response.status_code == 401


# ============================================================
# TEST 2 - EMPTY DASHBOARD
# ============================================================

def test_dashboard_authenticated():

    token = get_auth_token(
        "dashboard-empty@example.com"
    )

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert "user" in data
    assert "stats" in data
    assert "recent_progress" in data
    assert "message" in data

    assert data["user"]["email"] == (
        "dashboard-empty@example.com"
    )

    assert data["user"]["role"] == "student"

    assert data["stats"]["courses_enrolled"] == 0
    assert data["stats"]["courses_completed"] == 0
    assert data["stats"]["overall_progress"] == 0.0
    assert data["stats"]["circuits_created"] == 0
    assert data["stats"]["simulations_run"] == 0

    assert data["recent_progress"] == []


# ============================================================
# TEST 3 - DASHBOARD WITH COURSE PROGRESS
# ============================================================

def test_dashboard_with_progress():

    token = get_auth_token(
        "dashboard-progress@example.com"
    )

    user_id = create_test_user(
        email="dashboard-progress@example.com"
    )

    db = TestingSessionLocal()

    try:

        course = Course(
            title="Quantum Fundamentals",
            description=(
                "Introduction to quantum computing"
            ),
            level="beginner",
            duration="4 weeks",
            category="quantum-computing",
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        # IMPORTANT:
        # Store the ID while the SQLAlchemy session
        # is still active.
        course_id = course.id

        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            status="active",
        )

        progress = Progress(
            user_id=user_id,
            course_id=course_id,
            completion_percentage=50.0,
            completed_lessons=5,
            status="in_progress",
        )

        db.add(enrollment)
        db.add(progress)
        db.commit()

    finally:
        db.close()

    # --------------------------------------------------------
    # Request dashboard
    # --------------------------------------------------------

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    # --------------------------------------------------------
    # Check statistics
    # --------------------------------------------------------

    assert data["stats"]["courses_enrolled"] == 1
    assert data["stats"]["courses_completed"] == 0
    assert data["stats"]["overall_progress"] == 50.0

    # --------------------------------------------------------
    # Check recent progress
    # --------------------------------------------------------

    assert len(data["recent_progress"]) == 1

    recent = data["recent_progress"][0]

    assert recent["course_id"] == course_id
    assert recent["course_title"] == (
        "Quantum Fundamentals"
    )
    assert recent["completion_percentage"] == 50.0
    assert recent["completed_lessons"] == 5
    assert recent["status"] == "in_progress"

# ============================================================
# TEST 4 - COMPLETED COURSE
# ============================================================

def test_dashboard_completed_course():

    token = get_auth_token(
        "dashboard-completed@example.com"
    )

    user_id = create_test_user(
        email="dashboard-completed@example.com"
    )

    db = TestingSessionLocal()

    try:

        course = Course(
            title="Quantum Algorithms",
            description=(
                "Introduction to quantum algorithms"
            ),
            level="intermediate",
            duration="6 weeks",
            category="quantum-algorithms",
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        enrollment = Enrollment(
            user_id=user_id,
            course_id=course.id,
            status="active",
        )

        progress = Progress(
            user_id=user_id,
            course_id=course.id,
            completion_percentage=100.0,
            completed_lessons=10,
            status="completed",
        )

        db.add(enrollment)
        db.add(progress)
        db.commit()

    finally:
        db.close()

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["stats"]["courses_enrolled"] == 1
    assert data["stats"]["courses_completed"] == 1
    assert data["stats"]["overall_progress"] == 100.0


# ============================================================
# TEST 5 - CIRCUIT COUNT
# ============================================================

def test_dashboard_circuit_count():

    token = get_auth_token(
        "dashboard-circuits@example.com"
    )

    user_id = create_test_user(
        email="dashboard-circuits@example.com"
    )

    db = TestingSessionLocal()

    try:

        db.add_all(
            [
                Circuit(
                    user_id=user_id,
                    name="Circuit 1",
                    description="Test circuit",
                    circuit_data='{"qubits": 1}',
                ),
                Circuit(
                    user_id=user_id,
                    name="Circuit 2",
                    description="Test circuit",
                    circuit_data='{"qubits": 2}',
                ),
            ]
        )

        db.commit()

    finally:
        db.close()

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["stats"]["circuits_created"] == 2


# ============================================================
# TEST 6 - SIMULATION COUNT
# ============================================================

def test_dashboard_simulation_count():

    token = get_auth_token(
        "dashboard-simulations@example.com"
    )

    user_id = create_test_user(
        email="dashboard-simulations@example.com"
    )

    db = TestingSessionLocal()

    try:

        circuit = Circuit(
            user_id=user_id,
            name="Simulation Circuit",
            description="Test circuit",
            circuit_data='{"qubits": 1}',
        )

        db.add(circuit)
        db.commit()
        db.refresh(circuit)

        db.add_all(
            [
                Simulation(
                    user_id=user_id,
                    circuit_id=circuit.id,
                    job_id="dashboard-test-job-1",
                    backend="qiskit",
                    shots=100,
                    status="completed",
                    result_data='{"0": 100}',
                ),
                Simulation(
                    user_id=user_id,
                    circuit_id=circuit.id,
                    job_id="dashboard-test-job-2",
                    backend="qiskit",
                    shots=200,
                    status="completed",
                    result_data='{"0": 200}',
                ),
            ]
        )

        db.commit()

    finally:
        db.close()

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["stats"]["circuits_created"] == 1
    assert data["stats"]["simulations_run"] == 2


# ============================================================
# TEST 7 - USER ISOLATION
# ============================================================

def test_dashboard_user_isolation():

    token1 = get_auth_token(
        "dashboard-user-one@example.com"
    )

    user1_id = create_test_user(
        email="dashboard-user-one@example.com"
    )

    token2 = get_auth_token(
        "dashboard-user-two@example.com"
    )

    user2_id = create_test_user(
        email="dashboard-user-two@example.com"
    )

    db = TestingSessionLocal()

    try:

        db.add(
            Circuit(
                user_id=user1_id,
                name="User 1 Circuit",
                description="Private circuit",
                circuit_data='{"qubits": 1}',
            )
        )

        db.add(
            Circuit(
                user_id=user2_id,
                name="User 2 Circuit",
                description="Private circuit",
                circuit_data='{"qubits": 1}',
            )
        )

        db.commit()

    finally:
        db.close()

    response1 = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token1}"
        },
    )

    response2 = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token2}"
        },
    )

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    assert data1["user"]["email"] == (
        "dashboard-user-one@example.com"
    )

    assert data2["user"]["email"] == (
        "dashboard-user-two@example.com"
    )

    assert data1["stats"]["circuits_created"] == 1
    assert data2["stats"]["circuits_created"] == 1