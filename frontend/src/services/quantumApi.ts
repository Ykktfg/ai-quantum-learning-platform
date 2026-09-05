const API_URL = "http://127.0.0.1:8000"

export interface QuantumGate {
  gate: string
  qubit?: number
  control?: number
  target?: number
  qubit1?: number
  qubit2?: number
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
  counts: Record<string, number>
  shots: number
  num_qubits: number
  depth: number
  size: number
  statevector: ComplexNumber[]
  circuit: string
}

export async function simulateCircuit(
  payload: CustomCircuitRequest | AlgorithmRequest
): Promise<SimulationResult> {
  const response = await fetch(`${API_URL}/simulate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.text()
    throw new Error(error || "Simulation failed")
  }

  return response.json()
}