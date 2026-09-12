import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """
    Backend client for communicating with the teammate's AI service.

    The AI service owns all LLM/RAG logic.
    This client only handles HTTP communication, validation,
    timeouts, and controlled error handling.
    """

    def __init__(self):
        self.base_url = os.getenv(
            "AI_API_URL",
            "http://127.0.0.1:8002",
        ).rstrip("/")

        self.timeout = float(
            os.getenv("AI_API_TIMEOUT", "60")
        )

    def _post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        url = f"{self.base_url}{endpoint}"

        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Unable to connect to AI API at {self.base_url}"
            ) from exc

        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text

            raise RuntimeError(
                f"AI API returned HTTP {response.status_code}: {detail}"
            )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "AI API returned invalid JSON"
            ) from exc

        if not isinstance(result, dict):
            raise RuntimeError(
                "AI API returned an invalid response format"
            )

        if result.get("error"):
            raise RuntimeError(
                f"AI API request failed: {result['error']}"
            )

        return result

    def chat(
        self,
        question: str,
        quantum_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        return self._post(
            "/api/ai/tutor/chat",
            {
                "question": question,
                "quantum_context": quantum_context or {},
            },
        )

    def explain_circuit(
        self,
        circuit: str,
        quantum_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if not circuit or not circuit.strip():
            raise ValueError("Circuit cannot be empty")

        return self._post(
            "/api/ai/tutor/explain-circuit",
            {
                "circuit": circuit,
                "quantum_context": quantum_context or {},
            },
        )

    def debug(
        self,
        code: str,
        error: str,
        quantum_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if not code or not code.strip():
            raise ValueError("Code cannot be empty")

        if not error or not error.strip():
            raise ValueError("Error cannot be empty")

        return self._post(
            "/api/ai/tutor/debug",
            {
                "code": code,
                "error": error,
                "quantum_context": quantum_context or {},
            },
        )

    def generate_code(
        self,
        request: str,
        quantum_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if not request or not request.strip():
            raise ValueError("Code generation request cannot be empty")

        return self._post(
            "/api/ai/tutor/generate-code",
            {
                "request": request,
                "quantum_context": quantum_context or {},
            },
        )


ai_client = AIClient()