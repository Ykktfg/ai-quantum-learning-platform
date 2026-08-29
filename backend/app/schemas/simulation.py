from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    backend: str = Field(
        default="qiskit",
        min_length=1,
        max_length=50,
    )

    shots: int = Field(
        default=1024,
        ge=1,
        le=100000,
    )


class SimulationResponse(BaseModel):
    id: int
    user_id: int
    circuit_id: int
    job_id: str
    backend: str
    shots: int
    status: str
    counts: dict