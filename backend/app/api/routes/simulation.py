import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import Circuit
from app.repositories.simulation_repository import (
    simulation_repository,
)
from app.services.simulation_service import simulation_service


router = APIRouter()


# ============================================================
# SIMULATION REQUEST
# ============================================================

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


# ============================================================
# HELPER - GET USER ID
# ============================================================

def get_authenticated_user_id(
    current_user: dict,
) -> int:
    """
    Extract and validate the authenticated user's ID.
    """

    user_id = current_user.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    try:
        return int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in authentication token",
        )


# ============================================================
# RUN CIRCUIT SIMULATION
# ============================================================

@router.post(
    "/circuits/{circuit_id}/simulate"
)
def simulate_circuit(
    circuit_id: int,
    request: SimulationRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Run a quantum circuit using Qiskit Aer
    and permanently save the result.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    # --------------------------------------------------------
    # Validate circuit ID
    # --------------------------------------------------------

    if circuit_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid circuit ID",
        )

    # --------------------------------------------------------
    # Find circuit
    # --------------------------------------------------------

    circuit = (
        db.query(Circuit)
        .filter(Circuit.id == circuit_id)
        .first()
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found",
        )

    # --------------------------------------------------------
    # Ownership protection
    # --------------------------------------------------------

    if circuit.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You do not have permission "
                "to simulate this circuit"
            ),
        )

    # --------------------------------------------------------
    # Validate backend
    # --------------------------------------------------------

    backend = request.backend.lower().strip()

    if backend not in ["qiskit"]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported simulation backend: {backend}. "
                "Currently supported backend: qiskit"
            ),
        )

    # --------------------------------------------------------
    # Run simulation
    # --------------------------------------------------------

    try:

        result = simulation_service.submit_simulation(
            circuit_id=circuit_id,
            circuit_data=circuit.circuit_data,
            backend=backend,
            shots=request.shots,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid circuit or simulation request: "
                f"{str(exc)}"
            ),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(exc)}",
        )

    # --------------------------------------------------------
    # Validate result
    # --------------------------------------------------------

    job_id = result.get("job_id")

    if not job_id:
        raise HTTPException(
            status_code=500,
            detail=(
                "Simulation service did not return "
                "a job ID"
            ),
        )

    simulation_status = result.get(
        "status",
        "completed",
    )

    counts = result.get(
        "counts",
        {},
    )

    if not isinstance(counts, dict):
        counts = {}

    # --------------------------------------------------------
    # SAVE USING REPOSITORY
    # --------------------------------------------------------

    try:

        simulation = simulation_repository.create(
            db=db,
            user_id=user_id,
            circuit_id=circuit_id,
            job_id=job_id,
            backend=backend,
            shots=request.shots,
            status=simulation_status,
            counts=counts,
        )

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save simulation result: "
                f"{str(exc)}"
            ),
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    simulation_response = {
        **result,

        "id": simulation.id,
        "user_id": simulation.user_id,
        "circuit_id": simulation.circuit_id,
        "job_id": simulation.job_id,
        "backend": simulation.backend,
        "shots": simulation.shots,
        "status": simulation.status,
        "counts": counts,
    }

    return {
        "success": True,
        "message": (
            "Circuit simulation completed successfully"
        ),
        "simulation": simulation_response,
    }


# ============================================================
# GET SIMULATION RESULTS FOR A CIRCUIT
# ============================================================

@router.get(
    "/circuits/{circuit_id}/results"
)
def get_simulation_results(
    circuit_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all saved simulation results
    for a circuit.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    # --------------------------------------------------------
    # Validate circuit ID
    # --------------------------------------------------------

    if circuit_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid circuit ID",
        )

    # --------------------------------------------------------
    # Find circuit
    # --------------------------------------------------------

    circuit = (
        db.query(Circuit)
        .filter(Circuit.id == circuit_id)
        .first()
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found",
        )

    # --------------------------------------------------------
    # Ownership protection
    # --------------------------------------------------------

    if circuit.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You do not have permission "
                "to access this circuit"
            ),
        )

    # --------------------------------------------------------
    # GET USING REPOSITORY
    # --------------------------------------------------------

    simulations = simulation_repository.get_by_circuit(
        db=db,
        circuit_id=circuit_id,
        user_id=user_id,
    )

    results = []

    for simulation in simulations:

        try:

            counts = (
                json.loads(simulation.result_data)
                if simulation.result_data
                else {}
            )

        except (
            json.JSONDecodeError,
            TypeError,
        ):

            counts = {}

        results.append(
            {
                "id": simulation.id,
                "job_id": simulation.job_id,
                "circuit_id": simulation.circuit_id,
                "user_id": simulation.user_id,
                "backend": simulation.backend,
                "shots": simulation.shots,
                "status": simulation.status,
                "counts": counts,
            }
        )

    return {
        "success": True,
        "circuit_id": circuit_id,
        "total_simulations": len(results),
        "results": results,
    }


# ============================================================
# GET MY SIMULATIONS
# ============================================================

@router.get(
    "/simulations/me"
)
def get_my_simulations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all simulations created by
    the authenticated user.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    # --------------------------------------------------------
    # GET USING REPOSITORY
    # --------------------------------------------------------

    simulations = simulation_repository.get_by_user(
        db=db,
        user_id=user_id,
    )

    simulation_results = []

    for simulation in simulations:

        try:

            counts = (
                json.loads(simulation.result_data)
                if simulation.result_data
                else {}
            )

        except (
            json.JSONDecodeError,
            TypeError,
        ):

            counts = {}

        simulation_results.append(
            {
                "id": simulation.id,
                "job_id": simulation.job_id,
                "circuit_id": simulation.circuit_id,
                "user_id": simulation.user_id,
                "backend": simulation.backend,
                "shots": simulation.shots,
                "status": simulation.status,
                "counts": counts,
            }
        )

    return {
        "success": True,
        "total_simulations": len(
            simulation_results
        ),
        "simulations": simulation_results,
    }