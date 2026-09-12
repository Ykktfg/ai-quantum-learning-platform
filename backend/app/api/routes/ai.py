from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth.security import get_current_user
from app.services.ai_client import ai_client


router = APIRouter()


class AIChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    quantum_context: dict[str, Any] = Field(default_factory=dict)


class ExplainCircuitRequest(BaseModel):
    circuit: str = Field(..., min_length=1)
    quantum_context: dict[str, Any] = Field(default_factory=dict)


class AIDebugRequest(BaseModel):
    code: str = Field(..., min_length=1)
    error: str = Field(..., min_length=1)
    quantum_context: dict[str, Any] = Field(default_factory=dict)


class GenerateCodeRequest(BaseModel):
    request: str = Field(..., min_length=1)
    quantum_context: dict[str, Any] = Field(default_factory=dict)


def _handle_ai_error(exc: Exception) -> HTTPException:
    message = str(exc)

    if message.startswith("Unable to connect to AI API"):
        return HTTPException(
            status_code=502,
            detail=f"AI service unavailable: {message}",
        )

    if message.startswith("AI API returned HTTP"):
        return HTTPException(
            status_code=502,
            detail=message,
        )

    if message.startswith("AI API"):
        return HTTPException(
            status_code=502,
            detail=message,
        )

    return HTTPException(
        status_code=500,
        detail=f"AI integration error: {message}",
    )


@router.post("/ai/tutor/chat")
def tutor_chat(
    request: AIChatRequest,
    current_user=Depends(get_current_user),
):
    try:
        return ai_client.chat(
            question=request.question,
            quantum_context=request.quantum_context,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_ai_error(exc) from exc


@router.post("/ai/tutor/explain-circuit")
def explain_circuit(
    request: ExplainCircuitRequest,
    current_user=Depends(get_current_user),
):
    try:
        return ai_client.explain_circuit(
            circuit=request.circuit,
            quantum_context=request.quantum_context,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_ai_error(exc) from exc


@router.post("/ai/tutor/debug")
def debug_code(
    request: AIDebugRequest,
    current_user=Depends(get_current_user),
):
    try:
        return ai_client.debug(
            code=request.code,
            error=request.error,
            quantum_context=request.quantum_context,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_ai_error(exc) from exc


@router.post("/ai/tutor/generate-code")
def generate_code(
    request: GenerateCodeRequest,
    current_user=Depends(get_current_user),
):
    try:
        return ai_client.generate_code(
            request=request.request,
            quantum_context=request.quantum_context,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise _handle_ai_error(exc) from exc