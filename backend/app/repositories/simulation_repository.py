import json

from sqlalchemy.orm import Session

from app.db.models import Simulation


class SimulationRepository:
    """
    Database repository for quantum simulations.
    """

    # ========================================================
    # CREATE SIMULATION
    # ========================================================

    def create(
        self,
        db: Session,
        user_id: int,
        circuit_id: int,
        job_id: str,
        backend: str,
        shots: int,
        status: str,
        counts: dict,
    ) -> Simulation:
        """
        Create and save a simulation result.
        """

        simulation = Simulation(
            user_id=user_id,
            circuit_id=circuit_id,
            job_id=job_id,
            backend=backend,
            shots=shots,
            status=status,
            result_data=json.dumps(counts),
        )

        db.add(simulation)
        db.commit()
        db.refresh(simulation)

        return simulation

    # ========================================================
    # GET SIMULATIONS FOR CIRCUIT
    # ========================================================

    def get_by_circuit(
        self,
        db: Session,
        circuit_id: int,
        user_id: int,
    ) -> list[Simulation]:
        """
        Return simulations for a user's circuit.
        """

        return (
            db.query(Simulation)
            .filter(
                Simulation.circuit_id == circuit_id,
                Simulation.user_id == user_id,
            )
            .order_by(Simulation.id.desc())
            .all()
        )

    # ========================================================
    # GET USER SIMULATIONS
    # ========================================================

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Simulation]:
        """
        Return all simulations belonging to a user.
        """

        return (
            db.query(Simulation)
            .filter(
                Simulation.user_id == user_id
            )
            .order_by(Simulation.id.desc())
            .all()
        )

    # ========================================================
    # GET SIMULATION BY ID
    # ========================================================

    def get_by_id(
        self,
        db: Session,
        simulation_id: int,
    ) -> Simulation | None:
        """
        Return a simulation by ID.
        """

        return (
            db.query(Simulation)
            .filter(
                Simulation.id == simulation_id
            )
            .first()
        )


simulation_repository = SimulationRepository()