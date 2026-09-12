from unittest.mock import patch

import pytest

from app.services.quantum_client import QuantumClient


def test_build_simulation_payload():
    client = QuantumClient()

    circuit = {
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

    payload = client.build_simulation_payload(
        circuit,
        shots=100,
    )

    assert payload["algorithm"] is None
    assert payload["qubits"] == 2
    assert payload["shots"] == 100

    assert payload["gates"][0] == {
        "gate": "H",
        "qubit": 0,
    }

    assert payload["gates"][1] == {
        "gate": "CX",
        "control": 0,
        "target": 1,
    }


def test_convert_supported_gates():
    client = QuantumClient()

    assert client.convert_gate(
        {
            "type": "H",
            "target": 0,
        }
    ) == {
        "gate": "H",
        "qubit": 0,
    }

    assert client.convert_gate(
        {
            "type": "CNOT",
            "control": 0,
            "target": 1,
        }
    ) == {
        "gate": "CX",
        "control": 0,
        "target": 1,
    }


def test_convert_rotation_gate():
    client = QuantumClient()

    result = client.convert_gate(
        {
            "type": "RX",
            "target": 0,
            "angle": 1.57,
        }
    )

    assert result == {
        "gate": "RX",
        "qubit": 0,
        "angle": 1.57,
    }


def test_unsupported_gate():
    client = QuantumClient()

    with pytest.raises(ValueError):
        client.convert_gate(
            {
                "type": "UNKNOWN_GATE",
                "target": 0,
            }
        )


@patch("app.services.quantum_client.httpx.post")
def test_simulate_success(mock_post):
    client = QuantumClient()

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "algorithm": "custom",
        "simulation": {
            "counts": {
                "00": 51,
                "11": 49,
            },
            "probabilities": {
                "00": 0.51,
                "11": 0.49,
            },
            "shots": 100,
        },
    }

    circuit = {
        "qubits": 2,
        "gates": [
            {
                "type": "H",
                "target": 0,
            },
            {
                "type": "CX",
                "control": 0,
                "target": 1,
            },
        ],
    }

    result = client.simulate(
        circuit,
        shots=100,
    )

    assert result["algorithm"] == "custom"
    assert result["simulation"]["shots"] == 100
    assert result["simulation"]["counts"]["00"] == 51
    assert result["simulation"]["counts"]["11"] == 49

    mock_post.assert_called_once()


@patch("app.services.quantum_client.httpx.post")
def test_simulate_quantum_api_error(mock_post):
    client = QuantumClient()

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "error": "Invalid quantum circuit",
    }

    circuit = {
        "qubits": 2,
        "gates": [],
    }

    with pytest.raises(
        RuntimeError,
        match="Quantum API simulation failed",
    ):
        client.simulate(
            circuit,
            shots=100,
        )


@patch("app.services.quantum_client.httpx.post")
def test_simulate_http_error(mock_post):
    client = QuantumClient()

    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal quantum service error"
    mock_post.return_value.json.return_value = {
        "detail": "Internal quantum service error",
    }

    circuit = {
        "qubits": 2,
        "gates": [],
    }

    with pytest.raises(
        RuntimeError,
        match="Quantum API returned HTTP 500",
    ):
        client.simulate(
            circuit,
            shots=100,
        )