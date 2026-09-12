const API_URL = "http://127.0.0.1:8000"

export interface QuantumGate {
  gate: string

  // Single-qubit gates
  qubit?: number

  // Controlled gates / SWAP
  control?: number
  target?: number

  // Backward compatibility
  qubit1?: number
  qubit2?: number

  // CCX / Toffoli
  control1?: number
  control2?: number

  // Rotation gates
  angle?: number
}

export interface CustomCircuitRequest {
  qubits: number
  gates: QuantumGate[]
  shots: number
}

export interface AlgorithmRequest {
  algorithm: "superposition" | "bell" | "ghz"
  shots?: number
}

export interface ComplexNumber {
  real: number
  imag: number
}

export interface SimulationResult {
  algorithm: string

  simulation: {
    counts: Record<string, number>
    probabilities: Record<string, number>
    shots: number
  }

  circuit: {
    num_qubits: number
    depth: number
    size: number
    total_gates: number
    gate_counts: Record<string, number>
  }

  state: {
    statevector: ComplexNumber[]
    nonzero_states: Record<string, number>
    probabilities: Record<string, number>
    total_probability: number
    is_normalized: boolean
    state_expression: string
  }

  measurement: {
    most_likely_state: string
    most_likely_probability: number
    entropy: number
    distribution: string
    interpretation: string
  }

  education: {
    has_superposition: boolean
    has_entanglement: boolean
    explanation: string
  }

  circuit_explanation: string
  circuit_diagram: string
}

export async function simulateCircuit(
  payload: CustomCircuitRequest | AlgorithmRequest,
): Promise<SimulationResult> {
  let response: Response

  try {
    response = await fetch(`${API_URL}/simulate`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(payload),
    })
  } catch (error) {
    throw new Error(
      "Cannot connect to the Quantum Engine. Make sure the FastAPI server is running on port 8000.",
    )
  }

  if (!response.ok) {
    let errorMessage = "Simulation failed"

    try {
      const error = await response.json()

      if (typeof error?.detail === "string") {
        errorMessage = error.detail
      } else if (error?.detail) {
        errorMessage = JSON.stringify(error.detail)
      } else {
        errorMessage = JSON.stringify(error)
      }
    } catch {
      try {
        const errorText = await response.text()

        if (errorText) {
          errorMessage = errorText
        }
      } catch {
        // Keep default error message
      }
    }

    throw new Error(
      `${errorMessage} (HTTP ${response.status})`,
    )
  }

  try {
    return (await response.json()) as SimulationResult
  } catch {
    throw new Error(
      "The Quantum Engine returned an invalid response.",
    )
  }
}