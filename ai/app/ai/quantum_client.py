import httpx


QUANTUM_API_URL = "http://127.0.0.1:8001"


def simulate_algorithm(algorithm: str, shots: int = 1000) -> dict:
    response = httpx.post(
        f"{QUANTUM_API_URL}/simulate",
        json={
            "algorithm": algorithm,
            "shots": shots,
        },
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()
