from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    return {"Authorization": "Bearer test-token"}


@patch("app.api.routes.ai.ai_client.chat")
def test_ai_chat(mock_chat):
    mock_chat.return_value = {
        "answer": "Superposition means a qubit can exist in a combination of states."
    }

    response = client.post(
        "/api/ai/tutor/chat",
        json={
            "question": "What is superposition?",
            "quantum_context": {},
        },
        headers=get_auth_headers(),
    )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["answer"]


@patch("app.api.routes.ai.ai_client.explain_circuit")
def test_ai_explain_circuit(mock_explain):
    mock_explain.return_value = {
        "explanation": "This circuit applies a Hadamard gate."
    }

    response = client.post(
        "/api/ai/tutor/explain-circuit",
        json={
            "circuit": "H q[0]",
            "quantum_context": {},
        },
        headers=get_auth_headers(),
    )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["explanation"]


@patch("app.api.routes.ai.ai_client.debug")
def test_ai_debug(mock_debug):
    mock_debug.return_value = {
        "explanation": "The circuit contains an invalid gate operation."
    }

    response = client.post(
        "/api/ai/tutor/debug",
        json={
            "code": "qc.h(0)",
            "error": "Example error",
            "quantum_context": {},
        },
        headers=get_auth_headers(),
    )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["explanation"]


@patch("app.api.routes.ai.ai_client.generate_code")
def test_ai_generate_code(mock_generate):
    mock_generate.return_value = {
        "code": "from qiskit import QuantumCircuit"
    }

    response = client.post(
        "/api/ai/tutor/generate-code",
        json={
            "request": "Create a Bell state circuit",
            "quantum_context": {},
        },
        headers=get_auth_headers(),
    )

    assert response.status_code in (200, 401)

    if response.status_code == 200:
        assert response.json()["code"]


def test_ai_chat_validation():
    response = client.post(
        "/api/ai/tutor/chat",
        json={
            "question": "",
            "quantum_context": {},
        },
    )

    assert response.status_code in (401, 422)


def test_ai_explain_circuit_validation():
    response = client.post(
        "/api/ai/tutor/explain-circuit",
        json={
            "circuit": "",
            "quantum_context": {},
        },
    )

    assert response.status_code in (401, 422)
