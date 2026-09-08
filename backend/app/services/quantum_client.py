import json
import os
from typing import Any

import httpx
from dotenv import load_dotenv


load_dotenv()


class QuantumClient:
    """
    Backend-side client for communicating with the
    Quantum team's FastAPI service.

    This file belongs to the backend only.
    It does not modify or implement the Quantum engine.
    """

    def __init__(self) -> None:
        self.base_url = os.getenv(
            "QUANTUM_API_URL",
            "http://127.0.0.1:8001",
        ).rstrip("/")

        self.timeout = float(
            os.getenv(
                "QUANTUM_API_TIMEOUT",
                "60",
            )
        )

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self) -> dict[str, Any]:
        """Check whether the Quantum API is available."""

        try:
            response = httpx.get(
                f"{self.base_url}/health",
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at "
                f"{self.base_url}"
            ) from exc

        if response.status_code >= 400:
            raise RuntimeError(
                f"Quantum API health check failed: "
                f"HTTP {response.status_code}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API health endpoint returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API health check failed: "
                f"{result['error']}"
            )

        return result

    # ========================================================
    def list_gates(self) -> Any:
        try:
            response = httpx.get(
                f"{self.base_url}/gates",
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at {self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"Quantum API returned HTTP {response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API gates endpoint returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API gates request failed: {result['error']}"
            )

        return result

    def get_gate(self, gate_name: str) -> Any:
        if not gate_name or not gate_name.strip():
            raise ValueError("Gate name cannot be empty")

        gate_name = gate_name.strip().upper()

        try:
            response = httpx.get(
                f"{self.base_url}/gates/{gate_name}",
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at {self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"Quantum API returned HTTP {response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API gate endpoint returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API gate request failed: {result['error']}"
            )

        return result

    def explain(self, payload: dict[str, Any]) -> Any:
        if not isinstance(payload, dict):
            raise ValueError(
                "Quantum explanation payload must be an object"
            )

        try:
            response = httpx.post(
                f"{self.base_url}/explain",
                json=payload,
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at {self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"Quantum API returned HTTP {response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API explain endpoint returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API explanation failed: {result['error']}"
            )

        return result

    def debug(self, payload: dict[str, Any]) -> Any:
        if not isinstance(payload, dict):
            raise ValueError(
                "Quantum debug payload must be an object"
            )

        try:
            response = httpx.post(
                f"{self.base_url}/debug",
                json=payload,
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at {self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"Quantum API returned HTTP {response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API debug endpoint returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API debugging failed: {result['error']}"
            )

        return result
    # GATE CONVERSION
    # ========================================================

    @staticmethod
    def convert_gate(
        gate: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert the backend gate representation into the
        format expected by the Quantum API.

        Backend:
            {"type": "H", "target": 0}

        Quantum API:
            {"gate": "H", "qubit": 0}
        """

        if not isinstance(gate, dict):
            raise ValueError(
                "Each quantum gate must be an object"
            )

        gate_type = str(
            gate.get("type", "")
        ).upper().strip()

        if not gate_type:
            raise ValueError(
                "Quantum gate must contain a valid 'type'"
            )

        target = gate.get("target")

        if not isinstance(target, int):
            raise ValueError(
                f"Gate {gate_type} requires an integer target"
            )

        # ----------------------------------------------------
        # Single-qubit gates
        # ----------------------------------------------------

        if gate_type in {
            "I",
            "H",
            "X",
            "Y",
            "Z",
            "S",
            "T",
            "SX",
        }:
            return {
                "gate": gate_type,
                "qubit": target,
            }

        # ----------------------------------------------------
        # Controlled gates
        # ----------------------------------------------------

        if gate_type in {
            "CX",
            "CNOT",
            "CY",
            "CZ",
            "CH",
        }:
            control = gate.get("control")

            if not isinstance(control, int):
                raise ValueError(
                    f"{gate_type} gate requires an integer control"
                )

            quantum_gate_type = (
                "CX"
                if gate_type == "CNOT"
                else gate_type
            )

            return {
                "gate": quantum_gate_type,
                "control": control,
                "target": target,
            }

        # ----------------------------------------------------
        # SWAP
        # ----------------------------------------------------

        if gate_type == "SWAP":
            control = gate.get("control")

            if not isinstance(control, int):
                raise ValueError(
                    "SWAP gate requires an integer control"
                )

            return {
                "gate": "SWAP",
                "control": control,
                "target": target,
            }

        # ----------------------------------------------------
        # Toffoli / CCX
        # ----------------------------------------------------

        if gate_type == "CCX":
            control1 = gate.get("control1")
            control2 = gate.get("control2")

            if not isinstance(control1, int):
                raise ValueError(
                    "CCX gate requires an integer control1"
                )

            if not isinstance(control2, int):
                raise ValueError(
                    "CCX gate requires an integer control2"
                )

            return {
                "gate": "CCX",
                "control1": control1,
                "control2": control2,
                "target": target,
            }

        # ----------------------------------------------------
        # Rotation gates
        # ----------------------------------------------------

        if gate_type in {
            "RX",
            "RY",
            "RZ",
        }:
            angle = gate.get("angle")

            if not isinstance(angle, (int, float)):
                raise ValueError(
                    f"{gate_type} gate requires a numeric angle"
                )

            return {
                "gate": gate_type,
                "qubit": target,
                "angle": angle,
            }

        raise ValueError(
            f"Unsupported quantum gate: {gate_type}"
        )

    # ========================================================
    # CIRCUIT CONVERSION
    # ========================================================

    def build_simulation_payload(
        self,
        circuit_data: str | dict[str, Any],
        shots: int,
    ) -> dict[str, Any]:
        """
        Convert the backend circuit into the request format
        expected by the Quantum API.
        """

        if isinstance(circuit_data, str):
            try:
                data = json.loads(circuit_data)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Invalid circuit data"
                ) from exc
        else:
            data = circuit_data

        if not isinstance(data, dict):
            raise ValueError(
                "Circuit data must be an object"
            )

        qubits = data.get("qubits")

        if not isinstance(qubits, int):
            raise ValueError(
                "Circuit must contain a valid integer 'qubits'"
            )

        if qubits < 1 or qubits > 20:
            raise ValueError(
                "Circuit qubits must be between 1 and 20"
            )

        gates = data.get("gates", [])

        if not isinstance(gates, list):
            raise ValueError(
                "Circuit 'gates' must be a list"
            )

        if shots < 1 or shots > 100000:
            raise ValueError(
                "Shots must be between 1 and 100000"
            )

        converted_gates = [
            self.convert_gate(gate)
            for gate in gates
        ]

        return {
            "algorithm": None,
            "qubits": qubits,
            "gates": converted_gates,
            "shots": shots,
        }

    # ========================================================
    # SIMULATION
    # ========================================================

    def simulate(
        self,
        circuit_data: str | dict[str, Any],
        shots: int,
    ) -> dict[str, Any]:
        """
        Send a circuit to the Quantum team's /simulate endpoint.

        Returns the raw successful Quantum API response.
        """

        payload = self.build_simulation_payload(
            circuit_data=circuit_data,
            shots=shots,
        )

        try:
            response = httpx.post(
                f"{self.base_url}/simulate",
                json=payload,
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to Quantum API at "
                f"{self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"Quantum API returned HTTP "
                f"{response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Quantum API returned invalid JSON"
            ) from exc

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(
                f"Quantum API simulation failed: "
                f"{result['error']}"
            )

        return result


quantum_client = QuantumClient()
