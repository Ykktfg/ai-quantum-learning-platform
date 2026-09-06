import json

from sqlalchemy.orm import Session

from app.db.models import Circuit


class CircuitRepository:
    """
    Database repository for quantum circuits.
    """

    # ========================================================
    # CREATE CIRCUIT
    # ========================================================

    def create(
        self,
        db: Session,
        user_id: int,
        circuit_data: dict,
    ) -> Circuit:
        """
        Create and save a circuit in the database.
        """

        circuit = Circuit(
            user_id=user_id,
            name=circuit_data["name"],
            description=circuit_data.get("description"),
            circuit_data=json.dumps(circuit_data),
        )

        db.add(circuit)
        db.commit()
        db.refresh(circuit)

        return circuit

    # ========================================================
    # GET CIRCUIT BY ID
    # ========================================================

    def get_by_id(
        self,
        db: Session,
        circuit_id: int,
    ) -> Circuit | None:
        """
        Get a circuit by its database ID.
        """

        return (
            db.query(Circuit)
            .filter(Circuit.id == circuit_id)
            .first()
        )

    # ========================================================
    # GET USER CIRCUITS
    # ========================================================

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Circuit]:
        """
        Get all circuits created by a user.
        """

        return (
            db.query(Circuit)
            .filter(Circuit.user_id == user_id)
            .order_by(Circuit.id.desc())
            .all()
        )

    # ========================================================
    # UPDATE CIRCUIT
    # ========================================================

    def update(
        self,
        db: Session,
        circuit: Circuit,
        circuit_data: dict,
    ) -> Circuit:
        """
        Update an existing circuit.
        """

        circuit.name = circuit_data["name"]

        circuit.description = circuit_data.get(
            "description"
        )

        circuit.circuit_data = json.dumps(
            circuit_data
        )

        db.commit()
        db.refresh(circuit)

        return circuit

    # ========================================================
    # DELETE CIRCUIT
    # ========================================================

    def delete(
        self,
        db: Session,
        circuit: Circuit,
    ) -> None:
        """
        Delete an existing circuit.
        """

        db.delete(circuit)
        db.commit()


circuit_repository = CircuitRepository()