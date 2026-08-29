# Quantum Engine

Starter quantum module for the AI Quantum Learning Platform.

## Run

Create/activate your `.venv`, then:

    pip install -r requirements.txt

Run the demos:

    python programs/superposition.py
    python programs/bell_state.py
    python programs/ghz_state.py
    python programs/quantum_teleportation.py
    python programs/deutsch_algorithm.py

Run all demos:

    python run_all.py

The code is intentionally separated into an engine and algorithm demos so it can later
be connected to the FastAPI backend and the React frontend.
