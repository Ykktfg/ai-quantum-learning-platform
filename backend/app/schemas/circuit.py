from pydantic import BaseModel, Field
from typing import Optional


class Gate(BaseModel):
    type: str = Field(..., description="Quantum gate type")
    target: int = Field(..., ge=0, description="Target qubit")

    control: Optional[int] = Field(
        default=None,
        ge=0,
        description="Control qubit for controlled gates"
    )


class CircuitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    qubits: int = Field(..., ge=1, le=20)
    gates: list[Gate] = Field(default_factory=list)