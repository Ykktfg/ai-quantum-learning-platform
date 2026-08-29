from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.repositories.circuit_repository import (
    circuit_repository,
)
from app.schemas.circuit import CircuitCreate


router = APIRouter()


# ============================================================
# HELPER - GET AUTHENTICATED USER ID
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
# CREATE CIRCUIT
# ============================================================

@router.post("/circuits")
def create_circuit(
    circuit: CircuitCreate,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Create and save a quantum circuit.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    circuit_data = circuit.model_dump()

    saved_circuit = circuit_repository.create(
        db=db,
        user_id=user_id,
        circuit_data=circuit_data,
    )

    return {
        "success": True,
        "message": "Circuit created successfully",
        "circuit": {
            "id": saved_circuit.id,
            "user_id": saved_circuit.user_id,
            "name": saved_circuit.name,
            "description": saved_circuit.description,
            "circuit_data": saved_circuit.circuit_data,
        },
    }


# ============================================================
# GET MY CIRCUITS
# ============================================================

@router.get("/circuits")
def get_my_circuits(
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Return all circuits belonging to the
    authenticated user.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    circuits = circuit_repository.get_by_user(
        db=db,
        user_id=user_id,
    )

    return {
        "success": True,
        "total_circuits": len(circuits),
        "circuits": [
            {
                "id": circuit.id,
                "user_id": circuit.user_id,
                "name": circuit.name,
                "description": circuit.description,
                "circuit_data": circuit.circuit_data,
            }
            for circuit in circuits
        ],
    }


# ============================================================
# GET ONE CIRCUIT
# ============================================================

@router.get("/circuits/{circuit_id}")
def get_circuit(
    circuit_id: int,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Get a specific circuit.

    Users can only access their own circuits.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    if circuit_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid circuit ID",
        )

    circuit = circuit_repository.get_by_id(
        db=db,
        circuit_id=circuit_id,
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found",
        )

    if circuit.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You do not have permission "
                "to access this circuit"
            ),
        )

    return {
        "success": True,
        "circuit": {
            "id": circuit.id,
            "user_id": circuit.user_id,
            "name": circuit.name,
            "description": circuit.description,
            "circuit_data": circuit.circuit_data,
        },
    }


# ============================================================
# UPDATE CIRCUIT
# ============================================================

@router.put("/circuits/{circuit_id}")
def update_circuit(
    circuit_id: int,
    circuit: CircuitCreate,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Update an existing quantum circuit.

    Users can only update their own circuits.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    if circuit_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid circuit ID",
        )

    existing_circuit = (
        circuit_repository.get_by_id(
            db=db,
            circuit_id=circuit_id,
        )
    )

    if existing_circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found",
        )

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if existing_circuit.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You do not have permission "
                "to update this circuit"
            ),
        )

    circuit_data = circuit.model_dump()

    updated_circuit = circuit_repository.update(
        db=db,
        circuit=existing_circuit,
        circuit_data=circuit_data,
    )

    return {
        "success": True,
        "message": "Circuit updated successfully",
        "circuit": {
            "id": updated_circuit.id,
            "user_id": updated_circuit.user_id,
            "name": updated_circuit.name,
            "description": updated_circuit.description,
            "circuit_data": (
                updated_circuit.circuit_data
            ),
        },
    }


# ============================================================
# DELETE CIRCUIT
# ============================================================

@router.delete("/circuits/{circuit_id}")
def delete_circuit(
    circuit_id: int,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Delete an existing quantum circuit.

    Users can only delete their own circuits.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    if circuit_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid circuit ID",
        )

    circuit = circuit_repository.get_by_id(
        db=db,
        circuit_id=circuit_id,
    )

    if circuit is None:
        raise HTTPException(
            status_code=404,
            detail="Circuit not found",
        )

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if circuit.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You do not have permission "
                "to delete this circuit"
            ),
        )

    # --------------------------------------------------------
    # Delete circuit
    # --------------------------------------------------------

    circuit_repository.delete(
        db=db,
        circuit=circuit,
    )

    return {
        "success": True,
        "message": "Circuit deleted successfully",
        "circuit_id": circuit_id,
    }