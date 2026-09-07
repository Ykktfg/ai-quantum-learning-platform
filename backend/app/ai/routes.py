from fastapi import APIRouter
from pydantic import BaseModel

from .tutor import (
    chat_with_tutor,
    explain_circuit,
    debug_quantum_code,
)

from .code_generator import generate_quantum_code


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


class ChatRequest(BaseModel):
    question: str
    quantum_context: dict | None = None


class ChatResponse(BaseModel):
    answer: str


class ExplainCircuitRequest(BaseModel):
    circuit: str
    quantum_context: dict | None = None


class ExplainCircuitResponse(BaseModel):
    explanation: str


class DebugRequest(BaseModel):
    code: str
    error: str | None = None
    quantum_context: dict | None = None


class DebugResponse(BaseModel):
    explanation: str


class CodeGenerationRequest(BaseModel):
    request: str
    quantum_context: dict | None = None


class CodeGenerationResponse(BaseModel):
    code: str


@router.post(
    "/tutor/chat",
    response_model=ChatResponse
)
def tutor_chat(request: ChatRequest):
    answer = chat_with_tutor(
        request.question,
        request.quantum_context
    )

    return {
        "answer": answer
    }


@router.post(
    "/tutor/explain-circuit",
    response_model=ExplainCircuitResponse
)
def tutor_explain_circuit(
    request: ExplainCircuitRequest
):
    explanation = explain_circuit(
        request.circuit,
        request.quantum_context
    )

    return {
        "explanation": explanation
    }


@router.post(
    "/tutor/debug",
    response_model=DebugResponse
)
def tutor_debug(request: DebugRequest):
    explanation = debug_quantum_code(
        request.code,
        request.error,
        request.quantum_context
    )

    return {
        "explanation": explanation
    }


@router.post(
    "/tutor/generate-code",
    response_model=CodeGenerationResponse
)
def tutor_generate_code(
    request: CodeGenerationRequest
):
    code = generate_quantum_code(
        request.request,
        request.quantum_context
    )

    return {
        "code": code
    }
