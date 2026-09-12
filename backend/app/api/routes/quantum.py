from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth.security import get_current_user
from app.services.quantum_client import quantum_client


router = APIRouter()


class QuantumExplainRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class QuantumDebugRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


def _handle_quantum_error(exc: RuntimeError) -> HTTPException:
    message = str(exc)

    if message.startswith("Unable to connect to Quantum API"):
        return HTTPException(
            status_code=502,
            detail=f"Quantum service unavailable: {message}",
        )

    if message.startswith("Quantum API returned HTTP"):
        return HTTPException(
            status_code=502,
            detail=message,
        )

    if message.startswith("Quantum API"):
        return HTTPException(
            status_code=502,
            detail=message,
        )

    return HTTPException(
        status_code=500,
        detail=f"Quantum integration error: {message}",
    )


@router.get("/quantum/health")
def quantum_health(
    current_user=Depends(get_current_user),
):
    try:
        return quantum_client.health()
    except RuntimeError as exc:
        raise _handle_quantum_error(exc) from exc


@router.get("/quantum/gates")
def list_quantum_gates(
    current_user=Depends(get_current_user),
):
    try:
        return quantum_client.list_gates()
    except RuntimeError as exc:
        raise _handle_quantum_error(exc) from exc


@router.get("/quantum/gates/{gate_name}")
def get_quantum_gate(
    gate_name: str,
    current_user=Depends(get_current_user),
):
    try:
        return quantum_client.get_gate(gate_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_quantum_error(exc) from exc


@router.post("/quantum/explain")
def explain_quantum(
    request: QuantumExplainRequest,
    current_user=Depends(get_current_user),
):
    try:
        return quantum_client.explain(request.payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_quantum_error(exc) from exc


@router.post("/quantum/debug")
def debug_quantum(
    request: QuantumDebugRequest,
    current_user=Depends(get_current_user),
):
    try:
        return quantum_client.debug(request.payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_quantum_error(exc) from exc
