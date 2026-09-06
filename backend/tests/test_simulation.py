from fastapi.testclient import TestClient

from app.main import app
from app.db.models import User, Circuit
from app.auth.security import hash_password

from tests.conftest import TestingSessionLocal


client = TestClient(app)


# ============================================================
# CONSTANTS
# ============================================================

TEST_EMAIL = "simulation-test@example.com"
TEST_PASSWORD = "TestPassword123"


# ============================================================
# CREATE TEST USER
# ============================================================

def create_test_user(
    email=TEST_EMAIL,
    name="Simulation Test Student",
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

    return response.json()["access_token"]


# ============================================================
# CIRCUIT PAYLOAD
# ============================================================

def circuit_payload(
    name="Simulation Test Circuit",
):
    return {
        "name": name,
        "qubits": 2,
        "gates": [
            {
                "type": "H",
                "target": 0,
            },
            {
                "type": "CX",
                "target": 1,
                "control": 0,
            },
        ],
    }


# ============================================================
# CREATE CIRCUIT HELPER
# ============================================================

def create_circuit(token):
    response = client.post(
        "/api/circuits",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=circuit_payload(),
    )

    assert response.status_code == 200, response.text

    return response.json()["circuit"]["id"]


# ============================================================
# TEST 1 - SIMULATE CIRCUIT
# ============================================================

def test_simulate_circuit():

    token = get_auth_token()

    circuit_id = create_circuit(token)

    response = client.post(
        f"/api/circuits/{circuit_id}/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "qiskit",
            "shots": 100,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Circuit simulation completed successfully"
    )

    simulation = data["simulation"]

    assert simulation["id"] > 0
    assert simulation["circuit_id"] == circuit_id
    assert simulation["user_id"] > 0
    assert simulation["backend"] == "qiskit"
    assert simulation["shots"] == 100
    assert simulation["job_id"]
    assert simulation["counts"]

    assert sum(
        simulation["counts"].values()
    ) == 100


# ============================================================
# TEST 2 - GET CIRCUIT SIMULATION RESULTS
# ============================================================

def test_get_simulation_results():

    token = get_auth_token()

    circuit_id = create_circuit(token)

    simulate_response = client.post(
        f"/api/circuits/{circuit_id}/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "qiskit",
            "shots": 50,
        },
    )

    assert simulate_response.status_code == 200

    response = client.get(
        f"/api/circuits/{circuit_id}/results",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["success"] is True
    assert data["circuit_id"] == circuit_id
    assert data["total_simulations"] >= 1
    assert len(data["results"]) >= 1

    result = data["results"][0]

    assert result["circuit_id"] == circuit_id
    assert result["backend"] == "qiskit"
    assert result["shots"] == 50
    assert result["counts"]


# ============================================================
# TEST 3 - GET MY SIMULATIONS
# ============================================================

def test_get_my_simulations():

    token = get_auth_token()

    circuit_id = create_circuit(token)

    response = client.post(
        f"/api/circuits/{circuit_id}/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "qiskit",
            "shots": 25,
        },
    )

    assert response.status_code == 200

    response = client.get(
        "/api/simulations/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["success"] is True
    assert data["total_simulations"] >= 1
    assert len(data["simulations"]) >= 1


# ============================================================
# TEST 4 - SIMULATION WITHOUT TOKEN
# ============================================================

def test_simulate_without_token():

    response = client.post(
        "/api/circuits/1/simulate",
        json={
            "backend": "qiskit",
            "shots": 10,
        },
    )

    assert response.status_code == 401


# ============================================================
# TEST 5 - INVALID CIRCUIT ID
# ============================================================

def test_simulate_invalid_circuit_id():

    token = get_auth_token()

    response = client.post(
        "/api/circuits/0/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "qiskit",
            "shots": 10,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Invalid circuit ID"


# ============================================================
# TEST 6 - NONEXISTENT CIRCUIT
# ============================================================

def test_simulate_nonexistent_circuit():

    token = get_auth_token()

    response = client.post(
        "/api/circuits/999999/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "qiskit",
            "shots": 10,
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Circuit not found"


# ============================================================
# TEST 7 - UNSUPPORTED BACKEND
# ============================================================

def test_simulate_unsupported_backend():

    token = get_auth_token()

    circuit_id = create_circuit(token)

    response = client.post(
        f"/api/circuits/{circuit_id}/simulate",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "backend": "invalid_backend",
            "shots": 10,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert "Unsupported simulation backend" in data["detail"]


# ============================================================
# TEST 8 - CIRCUIT OWNERSHIP PROTECTION
# ============================================================

def test_simulation_ownership_protection():

    token1 = get_auth_token(
        "simulation-owner@example.com"
    )

    circuit_id = create_circuit(token1)

    token2 = get_auth_token(
        "simulation-other@example.com"
    )

    response = client.post(
        f"/api/circuits/{circuit_id}/simulate",
        headers={
            "Authorization": f"Bearer {token2}"
        },
        json={
            "backend": "qiskit",
            "shots": 10,
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert (
        data["detail"]
        == "You do not have permission "
        "to simulate this circuit"
    )


# ============================================================
# TEST 9 - RESULTS OWNERSHIP PROTECTION
# ============================================================

def test_results_ownership_protection():

    token1 = get_auth_token(
        "simulation-results-owner@example.com"
    )

    circuit_id = create_circuit(token1)

    token2 = get_auth_token(
        "simulation-results-other@example.com"
    )

    response = client.get(
        f"/api/circuits/{circuit_id}/results",
        headers={
            "Authorization": f"Bearer {token2}"
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert (
        data["detail"]
        == "You do not have permission "
        "to access this circuit"
    )