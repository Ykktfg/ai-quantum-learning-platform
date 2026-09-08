import json
from unittest.mock import patch

import pytest

from app.services.simulation_service import SimulationService


def valid_circuit():
    return json.dumps(
        {
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
    )


def test_submit_simulation_success():
    service = SimulationService()

    quantum_result = {
        "algorithm": "custom",
        "simulation": {
            "counts": {
                "00": 48,
                "11": 52,
            },
            "probabilities": {
                "00": 0.48,
                "11": 0.52,
            },
            "shots": 100,
        },
    }

    with patch(
        "app.services.simulation_service.quantum_client.simulate",
        return_value=quantum_result,
    ):
        result = service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="qiskit",
            shots=100,
        )

    assert result["circuit_id"] == 5
    assert result["backend"] == "qiskit"
    assert result["shots"] == 100
    assert result["status"] == "completed"

    assert result["counts"] == {
        "00": 48,
        "11": 52,
    }

    assert result["job_id"].startswith("job-")


def test_submit_simulation_accepts_aer_backend():
    service = SimulationService()

    quantum_result = {
        "algorithm": "custom",
        "simulation": {
            "counts": {
                "00": 10,
                "11": 10,
            },
            "shots": 20,
        },
    }

    with patch(
        "app.services.simulation_service.quantum_client.simulate",
        return_value=quantum_result,
    ):
        result = service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="aer",
            shots=20,
        )

    assert result["backend"] == "aer"
    assert result["shots"] == 20
    assert result["counts"]["00"] == 10
    assert result["counts"]["11"] == 10


def test_invalid_circuit_id():
    service = SimulationService()

    with pytest.raises(
        ValueError,
        match="Circuit ID must be greater than 0",
    ):
        service.submit_simulation(
            circuit_id=0,
            circuit_data=valid_circuit(),
            backend="qiskit",
            shots=100,
        )


def test_invalid_backend():
    service = SimulationService()

    with pytest.raises(
        ValueError,
        match="Unsupported simulation backend",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="invalid",
            shots=100,
        )


def test_invalid_shots_zero():
    service = SimulationService()

    with pytest.raises(
        ValueError,
        match="Shots must be at least 1",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="qiskit",
            shots=0,
        )


def test_invalid_shots_too_large():
    service = SimulationService()

    with pytest.raises(
        ValueError,
        match="Shots cannot exceed 100000",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="qiskit",
            shots=100001,
        )


def test_invalid_circuit_json():
    service = SimulationService()

    with pytest.raises(
        ValueError,
        match="Invalid circuit data",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data="not-valid-json",
            backend="qiskit",
            shots=100,
        )


def test_zero_qubits_rejected():
    service = SimulationService()

    circuit = json.dumps(
        {
            "qubits": 0,
            "gates": [],
        }
    )

    with pytest.raises(
        ValueError,
        match="Circuit must contain at least one qubit",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data=circuit,
            backend="qiskit",
            shots=100,
        )


def test_invalid_gates_rejected():
    service = SimulationService()

    circuit = json.dumps(
        {
            "qubits": 2,
            "gates": "invalid",
        }
    )

    with pytest.raises(
        ValueError,
        match="Circuit 'gates' must be a list",
    ):
        service.submit_simulation(
            circuit_id=5,
            circuit_data=circuit,
            backend="qiskit",
            shots=100,
        )


def test_quantum_service_failure():
    service = SimulationService()

    with patch(
        "app.services.simulation_service.quantum_client.simulate",
        side_effect=RuntimeError("Connection failed"),
    ):
        with pytest.raises(
            RuntimeError,
            match="Quantum simulation service unavailable",
        ):
            service.submit_simulation(
                circuit_id=5,
                circuit_data=valid_circuit(),
                backend="qiskit",
                shots=100,
            )


def test_invalid_quantum_response():
    service = SimulationService()

    with patch(
        "app.services.simulation_service.quantum_client.simulate",
        return_value=None,
    ):
        with pytest.raises(RuntimeError):
            service.submit_simulation(
                circuit_id=5,
                circuit_data=valid_circuit(),
                backend="qiskit",
                shots=100,
            )


def test_missing_simulation_data():
    service = SimulationService()

    quantum_result = {
        "algorithm": "custom",
        "simulation": {},
    }

    with patch(
        "app.services.simulation_service.quantum_client.simulate",
        return_value=quantum_result,
    ):
        result = service.submit_simulation(
            circuit_id=5,
            circuit_data=valid_circuit(),
            backend="qiskit",
            shots=100,
        )

    assert result["circuit_id"] == 5
    assert result["status"] == "completed"
    assert result["counts"] == {}