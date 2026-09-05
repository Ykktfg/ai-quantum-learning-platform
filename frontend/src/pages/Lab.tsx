import { CircuitBoard } from 'lucide-react'
import { Chip } from '@/components/quantum-ui'
import { CircuitLab } from '@/components/circuit-lab'

export default function LabPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-primary">
            <CircuitBoard className="size-5" />
            <span className="text-sm font-medium tracking-wide">SIMULATION ENVIRONMENT</span>
          </div>
          <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">Quantum Circuit Lab</h1>
          <p className="mt-1 text-muted-foreground">
            Build, run and simulate real quantum circuits with a live state-vector engine.
          </p>
        </div>
        <Chip tone="cyan" className="w-fit">
          Live simulator · 3 qubits
        </Chip>
      </div>

      <CircuitLab />
    </div>
  )
}
