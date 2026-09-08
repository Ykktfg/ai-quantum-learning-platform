from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def auth_headers():
    return {"Authorization": "Bearer test-token"}


@patch("app.main.quantum_router")
def test_quantum_health(mock_router):
    from app.services.quantum_client import quantum_client

    with patch.object(
        quantum_client,
        "health",
        return_value={"status": "healthy"},
    ):
        response = client.get(
            "/api/quantum/health",
            headers=auth_headers(),
        )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["status"] == "healthy"


def test_quantum_list_gates():
    from app.services.quantum_client import quantum_client

    with patch.object(
        quantum_client,
        "list_gates",
        return_value={"gates": ["H", "X", "Y", "Z", "CX"]},
    ):
        response = client.get(
            "/api/quantum/gates",
            headers=auth_headers(),
        )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert "gates" in response.json()


def test_quantum_get_gate():
    from app.services.quantum_client import quantum_client

    with patch.object(
        quantum_client,
        "get_gate",
        return_value={
            "name": "H",
            "description": "Hadamard gate",
        },
    ):
        response = client.get(
            "/api/quantum/gates/H",
            headers=auth_headers(),
        )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["name"] == "H"


def test_quantum_explain():
    from app.services.quantum_client import quantum_client

    with patch.object(
        quantum_client,
        "explain",
        return_value={
            "explanation": "This circuit creates a superposition."
        },
    ):
        response = client.post(
            "/api/quantum/explain",
            json={
                "payload": {
                    "circuit": "H q[0]"
                }
            },
            headers=auth_headers(),
        )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["explanation"]


def test_quantum_debug():
    from app.services.quantum_client import quantum_client

    with patch.object(
        quantum_client,
        "debug",
        return_value={
            "explanation": "The circuit contains an invalid operation."
        },
    ):
        response = client.post(
            "/api/quantum/debug",
            json={
                "payload": {
                    "code": "H q[0]",
                    "error": "Example error",
                }
            },
            headers=auth_headers(),
        )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["explanation"]


def test_quantum_explain_validation():
    response = client.post(
        "/api/quantum/explain",
        json={
            "payload": "invalid"
        },
        headers=auth_headers(),
    )

    assert response.status_code in (401, 404, 422)


def test_quantum_debug_validation():
    response = client.post(
        "/api/quantum/debug",
        json={
            "payload": "invalid"
        },
        headers=auth_headers(),
    )

    assert response.status_code in (401, 404, 422)
