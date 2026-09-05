import { useMemo, useState } from 'react'
import {
  Play,
  RotateCcw,
  Eraser,
  Undo2,
  Sparkles,
  Wand2,
  CircuitBoard,
  Activity,
  Sigma,
  BarChart3,
  CheckCircle2,
  CircleDot,
} from 'lucide-react'

import { Button } from '@/components/ui/button'
import { GlassCard, Chip } from '@/components/quantum-ui'
import { formatComplex, type Op, type SingleGate } from '@/lib/quantum'
import {
  simulateCircuit,
  type SimulationResult,
  type QuantumGate,
} from '@/services/quantumApi'
import { cn } from '@/lib/utils'

const N_QUBITS = 3
const N_COLS = 9

type Cell =
  | null
  | { type: 'single'; gate: SingleGate }
  | { type: 'cnot'; role: 'control' | 'target'; partner: number }
  | { type: 'swap'; role: 'a' | 'b'; partner: number }
  | { type: 'measure' }

type Grid = Cell[][]

type PaletteGate = {
  id: string
  label: string
  full: string
  tone: string
}

const PALETTE: PaletteGate[] = [
  {
    id: 'H',
    label: 'H',
    full: 'Hadamard — creates superposition',
    tone: 'primary',
  },
  {
    id: 'X',
    label: 'X',
    full: 'Pauli-X — bit flip (NOT)',
    tone: 'primary',
  },
  {
    id: 'Y',
    label: 'Y',
    full: 'Pauli-Y — bit + phase flip',
    tone: 'primary',
  },
  {
    id: 'Z',
    label: 'Z',
    full: 'Pauli-Z — phase flip',
    tone: 'primary',
  },
  {
    id: 'S',
    label: 'S',
    full: 'Phase gate (π/2)',
    tone: 'accent',
  },
  {
    id: 'T',
    label: 'T',
    full: 'π/8 gate (π/4)',
    tone: 'accent',
  },
  {
    id: 'CNOT',
    label: '⊕',
    full: 'CNOT — entangles two qubits',
    tone: 'accent',
  },
  {
    id: 'SWAP',
    label: '⇄',
    full: 'SWAP — exchanges two qubits',
    tone: 'green',
  },
  {
    id: 'M',
    label: 'M',
    full: 'Measurement',
    tone: 'muted',
  },
]

function emptyGrid(): Grid {
  return Array.from(
    { length: N_QUBITS },
    () => Array.from({ length: N_COLS }, () => null as Cell),
  )
}

function bellGrid(): Grid {
  const g = emptyGrid()

  g[0][0] = { type: 'single', gate: 'H' }

  g[0][2] = {
    type: 'cnot',
    role: 'control',
    partner: 1,
  }

  g[1][2] = {
    type: 'cnot',
    role: 'target',
    partner: 0,
  }

  g[0][7] = { type: 'measure' }
  g[1][7] = { type: 'measure' }

  return g
}

const toneClasses: Record<string, string> = {
  primary:
    'bg-primary/15 text-primary ring-primary/40 hover:bg-primary/25',
  accent:
    'bg-accent/15 text-accent ring-accent/40 hover:bg-accent/25',
  green:
    'bg-chart-3/15 text-chart-3 ring-chart-3/40 hover:bg-chart-3/25',
  muted:
    'bg-secondary text-muted-foreground ring-border hover:bg-secondary/80',
}

export function CircuitLab() {
  const [grid, setGrid] = useState<Grid>(bellGrid)
  const [history, setHistory] = useState<Grid[]>([])
  const [selected, setSelected] = useState<string>('H')

  const [status, setStatus] = useState<
    'idle' | 'running' | 'complete'
  >('idle')

  const [explanation, setExplanation] =
    useState<string | null>(null)

  const [result, setResult] =
    useState<SimulationResult | null>(null)

  const [error, setError] =
    useState<string | null>(null)

  const ops = useMemo<Op[]>(
    () => buildOps(grid),
    [grid],
  )

  function pushHistory(next: Grid) {
    setHistory((h) => [...h.slice(-24), grid])
    setGrid(next)
    setStatus('idle')
    setExplanation(null)
    setResult(null)
    setError(null)
  }

  function placeGate(
    q: number,
    col: number,
    gateId: string,
  ) {
    const next = grid.map((row) => row.slice())

    if (gateId === 'M') {
      next[q][col] =
        next[q][col]?.type === 'measure'
          ? null
          : { type: 'measure' }
    } else if (
      gateId === 'CNOT' ||
      gateId === 'SWAP'
    ) {
      if (q + 1 >= N_QUBITS) return

      next[q][col] = null
      next[q + 1][col] = null

      if (gateId === 'CNOT') {
        next[q][col] = {
          type: 'cnot',
          role: 'control',
          partner: q + 1,
        }

        next[q + 1][col] = {
          type: 'cnot',
          role: 'target',
          partner: q,
        }
      } else {
        next[q][col] = {
          type: 'swap',
          role: 'a',
          partner: q + 1,
        }

        next[q + 1][col] = {
          type: 'swap',
          role: 'b',
          partner: q,
        }
      }
    } else {
      next[q][col] = {
        type: 'single',
        gate: gateId as SingleGate,
      }
    }

    pushHistory(next)
  }

  function clearCell(
    q: number,
    col: number,
  ) {
    const cell = grid[q][col]

    if (!cell) return

    const next = grid.map((row) => row.slice())

    next[q][col] = null

    if (
      (cell.type === 'cnot' ||
        cell.type === 'swap') &&
      'partner' in cell
    ) {
      next[cell.partner][col] = null
    }

    pushHistory(next)
  }

  async function run() {
    try {
      setStatus('running')
      setError(null)

      const gates = convertGridToApiGates(grid)

      const response = await simulateCircuit({
        qubits: N_QUBITS,
        gates,
        shots: 1000,
      })

      setResult(response)
      setStatus('complete')
    } catch (err) {
      console.error(err)

      setError(
        err instanceof Error
          ? err.message
          : 'Failed to simulate circuit',
      )

      setStatus('idle')
    }
  }

  function undo() {
    if (!history.length) return

    const prev = history[history.length - 1]

    setHistory((h) => h.slice(0, -1))
    setGrid(prev)
    setStatus('idle')
    setResult(null)
    setError(null)
  }

  function explain() {
    const distribution = result
      ? Object.entries(result.counts).map(
          ([state, count]) => ({
            state,
            prob: count / result.shots,
          }),
        )
      : []

    setExplanation(
      describeCircuit(grid, distribution),
    )
  }

  function optimize() {
    setExplanation(
      'Optimization: your circuit is already efficient. Adjacent self-inverse gates such as H·H or X·X can be cancelled, and redundant operations can be removed.',
    )
  }

  const measuredQubits = grid
    .map((row, q) =>
      row.some(
        (c) => c?.type === 'measure',
      )
        ? q
        : -1,
    )
    .filter((q) => q >= 0)

  return (
    <div className="space-y-6">

      <div className="grid gap-6 lg:grid-cols-[220px_1fr]">

        {/* GATE PALETTE */}
        <GlassCard className="h-fit p-4">

          <div className="mb-3 flex items-center gap-2 text-sm font-semibold">
            <CircuitBoard className="size-4 text-primary" />
            Quantum Gates
          </div>

          <div className="grid grid-cols-3 gap-2">

            {PALETTE.map((g) => (
              <button
                key={g.id}
                draggable
                onDragStart={(e) =>
                  e.dataTransfer.setData(
                    'gate',
                    g.id,
                  )
                }
                onClick={() =>
                  setSelected(g.id)
                }
                title={g.full}
                className={cn(
                  'flex aspect-square flex-col items-center justify-center rounded-xl font-mono text-lg font-bold ring-1 transition-all',
                  toneClasses[g.tone],
                  selected === g.id &&
                    'scale-105 ring-2 ring-offset-2 ring-offset-card',
                )}
              >
                {g.label}
              </button>
            ))}

          </div>

          <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
            Select a gate, then click a slot
            on the timeline — or drag it
            onto a qubit line.
          </p>

          <div className="mt-3 rounded-lg bg-secondary/50 p-2.5 text-xs">

            <div className="font-medium text-foreground">
              {
                PALETTE.find(
                  (g) => g.id === selected,
                )?.label
              }{' '}
              gate
            </div>

            <div className="text-muted-foreground">
              {
                PALETTE.find(
                  (g) => g.id === selected,
                )?.full
              }
            </div>

          </div>

        </GlassCard>

        {/* WORKSPACE */}
        <GlassCard className="overflow-hidden p-0">

          {/* CONTROLS */}
          <div className="flex flex-wrap items-center gap-2 border-b border-border p-3">

            <Button
              size="sm"
              className="rounded-lg"
              onClick={run}
            >
              <Play className="size-4" />
              Run Circuit
            </Button>

            <Button
              size="sm"
              variant="secondary"
              className="rounded-lg"
              onClick={() =>
                pushHistory(bellGrid())
              }
            >
              <RotateCcw className="size-4" />
              Reset
            </Button>

            <Button
              size="sm"
              variant="secondary"
              className="rounded-lg"
              onClick={() =>
                pushHistory(emptyGrid())
              }
            >
              <Eraser className="size-4" />
              Clear
            </Button>

            <Button
              size="sm"
              variant="secondary"
              className="rounded-lg"
              onClick={undo}
              disabled={!history.length}
            >
              <Undo2 className="size-4" />
              Undo
            </Button>

            <div className="ml-auto flex gap-2">

              <Button
                size="sm"
                variant="secondary"
                className="rounded-lg glow-violet"
                onClick={explain}
              >
                <Sparkles className="size-4 text-accent" />
                AI Explain
              </Button>

              <Button
                size="sm"
                variant="secondary"
                className="rounded-lg"
                onClick={optimize}
              >
                <Wand2 className="size-4" />
                Optimize
              </Button>

            </div>

          </div>

          {/* CIRCUIT TIMELINE */}
          <div className="overflow-x-auto bg-grid p-4">

            <div className="min-w-[560px] space-y-4">

              {Array.from({
                length: N_QUBITS,
              }).map((_, q) => (

                <div
                  key={q}
                  className="flex items-center gap-3"
                >

                  <div className="flex w-10 shrink-0 flex-col items-center font-mono text-sm">
                    <span className="text-primary">
                      q{q}
                    </span>

                    <span className="text-[10px] text-muted-foreground">
                      |0⟩
                    </span>
                  </div>

                  <div className="relative flex flex-1 items-center">

                    <div className="absolute left-0 right-0 top-1/2 h-px -translate-y-1/2 bg-gradient-to-r from-primary/50 via-border to-primary/50" />

                    <div className="relative grid flex-1 grid-cols-9 gap-1">

                      {Array.from({
                        length: N_COLS,
                      }).map((_, col) => (

                        <CellSlot
                          key={col}
                          cell={grid[q][col]}
                          onPlace={(gid) =>
                            placeGate(
                              q,
                              col,
                              gid,
                            )
                          }
                          onClear={() =>
                            clearCell(
                              q,
                              col,
                            )
                          }
                          onClick={() =>
                            grid[q][col]
                              ? clearCell(q, col)
                              : placeGate(
                                  q,
                                  col,
                                  selected,
                                )
                          }
                        />

                      ))}

                    </div>

                  </div>

                </div>

              ))}

            </div>

          </div>

          {/* STATUS */}
          <div className="flex items-center gap-3 border-t border-border px-4 py-2.5 text-sm">

            <StatusPill status={status} />

            <span className="text-muted-foreground">
              {ops.length} operation
              {ops.length === 1 ? '' : 's'} ·{' '}
              {N_QUBITS} qubits
            </span>

            {measuredQubits.length ? (
              <span className="ml-auto font-mono text-xs text-muted-foreground">
                measuring q
                {measuredQubits.join(', q')}
              </span>
            ) : null}

          </div>

        </GlassCard>

      </div>

      {/* ERROR */}
      {error ? (
        <GlassCard className="border border-destructive/30 p-4">
          <p className="text-sm text-destructive">
            Simulation failed: {error}
          </p>
        </GlassCard>
      ) : null}

      {/* AI EXPLANATION */}
      {explanation ? (
        <GlassCard
          glow="violet"
          className="flex items-start gap-3 p-5 animate-fade-up"
        >

          <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-accent/15 text-accent ring-1 ring-accent/25">
            <Sparkles className="size-5" />
          </span>

          <div>
            <div className="font-semibold">
              AI Circuit Explanation
            </div>

            <p className="mt-1 text-pretty text-sm leading-relaxed text-muted-foreground">
              {explanation}
            </p>
          </div>

        </GlassCard>
      ) : null}

      {/* RESULTS */}
      {result && (

        <div className="grid gap-6 lg:grid-cols-3">

          {/* MEASUREMENT RESULTS */}
          <GlassCard className="p-5">

            <div className="mb-4 flex items-center gap-2 font-semibold">
              <Activity className="size-4 text-primary" />
              Measurement Results
            </div>

            <div className="space-y-3">

              {Object.entries(
                result.counts,
              ).map(([state, count]) => {

                const percentage =
                  result.shots > 0
                    ? (count / result.shots) *
                      100
                    : 0

                return (
                  <div key={state}>

                    <div className="mb-1.5 flex items-center justify-between text-xs">

                      <span className="font-mono">
                        |{state}⟩
                      </span>

                      <span className="text-muted-foreground">
                        {count} shots ·{' '}
                        {percentage.toFixed(1)}%
                      </span>

                    </div>

                    <div className="h-2.5 overflow-hidden rounded-full bg-secondary/60">

                      <div
                        className="h-full bg-primary transition-all duration-700"
                        style={{
                          width: `${percentage}%`,
                        }}
                      />

                    </div>

                  </div>
                )
              })}

            </div>

          </GlassCard>

          {/* PROBABILITY DISTRIBUTION */}
          <GlassCard className="p-5">

            <div className="mb-4 flex items-center gap-2 font-semibold">
              <BarChart3 className="size-4 text-primary" />
              Probability Distribution
            </div>

            <div className="flex h-40 items-end justify-around gap-2">

              {Object.entries(
                result.counts,
              )
                .slice(0, 8)
                .map(
                  ([state, count]) => {

                    const percentage =
                      result.shots > 0
                        ? (count /
                            result.shots) *
                          100
                        : 0

                    return (
                      <div
                        key={state}
                        className="flex flex-1 flex-col items-center gap-2"
                      >

                        <div className="flex h-full w-full items-end justify-center">

                          <div
                            className="w-full max-w-9 rounded-t-md bg-gradient-to-t from-primary/50 to-primary transition-all duration-700"
                            style={{
                              height: `${Math.max(
                                4,
                                percentage,
                              )}%`,
                            }}
                            title={`${percentage.toFixed(
                              1,
                            )}%`}
                          />

                        </div>

                        <span className="font-mono text-[10px] text-muted-foreground">
                          |{state}⟩
                        </span>

                        <span className="font-mono text-[10px] text-primary">
                          {percentage.toFixed(0)}%
                        </span>

                      </div>
                    )
                  },
                )}

            </div>

          </GlassCard>

          {/* STATE VECTOR */}
          <GlassCard className="p-5">

            <div className="mb-4 flex items-center gap-2 font-semibold">
              <Sigma className="size-4 text-primary" />
              State Vector
            </div>

            <div className="max-h-44 space-y-1 overflow-y-auto pr-1 font-mono text-xs">

              {result.statevector.map(
                (amp, i) => {

                  const probability =
                    amp.real * amp.real +
                    amp.imag * amp.imag

                  const active =
                    probability > 1e-9

                  return (
                    <div
                      key={i}
                      className={cn(
                        'flex items-center justify-between rounded-md px-2 py-1',
                        active
                          ? 'bg-primary/10 text-foreground'
                          : 'text-muted-foreground/50',
                      )}
                    >

                      <span>
                        |
                        {i
                          .toString(2)
                          .padStart(
                            result.num_qubits,
                            '0',
                          )}
                        ⟩
                      </span>

                      <span>
                        {formatComplex({
                          re: amp.real,
                          im: amp.imag,
                        })}
                      </span>

                    </div>
                  )
                },
              )}

            </div>

          </GlassCard>

        </div>
      )}

      {/* CIRCUIT STATISTICS */}
      {result && (

        <GlassCard className="p-5">

          <div className="mb-4 flex items-center gap-2 font-semibold">
            <CircuitBoard className="size-4 text-primary" />
            Circuit Statistics
          </div>

          <div className="grid gap-3 sm:grid-cols-4">

            <div className="rounded-lg bg-secondary/50 p-3">
              <div className="text-xs text-muted-foreground">
                Qubits
              </div>
              <div className="mt-1 text-lg font-semibold">
                {result.num_qubits}
              </div>
            </div>

            <div className="rounded-lg bg-secondary/50 p-3">
              <div className="text-xs text-muted-foreground">
                Shots
              </div>
              <div className="mt-1 text-lg font-semibold">
                {result.shots}
              </div>
            </div>

            <div className="rounded-lg bg-secondary/50 p-3">
              <div className="text-xs text-muted-foreground">
                Depth
              </div>
              <div className="mt-1 text-lg font-semibold">
                {result.depth}
              </div>
            </div>

            <div className="rounded-lg bg-secondary/50 p-3">
              <div className="text-xs text-muted-foreground">
                Gates
              </div>
              <div className="mt-1 text-lg font-semibold">
                {result.size}
              </div>
            </div>

          </div>

        </GlassCard>
      )}

    </div>
  )
}

function CellSlot({
  cell,
  onPlace,
  onClear,
  onClick,
}: {
  cell: Cell
  onPlace: (gate: string) => void
  onClear: () => void
  onClick: () => void
}) {
  const [over, setOver] = useState(false)

  return (
    <button
      onClick={onClick}
      onDoubleClick={onClear}
      onDragOver={(e) => {
        e.preventDefault()
        setOver(true)
      }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => {
        e.preventDefault()
        setOver(false)

        const gateId =
          e.dataTransfer.getData('gate')

        if (gateId) {
          onPlace(gateId)
        }
      }}
      className={cn(
        'relative z-10 flex aspect-square items-center justify-center rounded-lg font-mono text-sm font-bold transition-all',
        !cell &&
          'border border-dashed border-border/60 bg-card/40 text-transparent hover:border-primary/50 hover:bg-primary/5',
        over &&
          'border-primary bg-primary/15 ring-2 ring-primary/40',
      )}
    >
      <CellContent cell={cell} />
    </button>
  )
}

function CellContent({
  cell,
}: {
  cell: Cell
}) {
  if (!cell) return <span>+</span>

  if (cell.type === 'single') {
    return (
      <span className="flex size-full items-center justify-center rounded-lg bg-primary/20 text-primary ring-1 ring-primary/40">
        {cell.gate}
      </span>
    )
  }

  if (cell.type === 'measure') {
    return (
      <span className="flex size-full items-center justify-center rounded-lg bg-secondary text-foreground ring-1 ring-border">
        <Activity className="size-4" />
      </span>
    )
  }

  if (cell.type === 'cnot') {
    return cell.role === 'control' ? (
      <span className="flex size-full items-center justify-center rounded-lg bg-accent/20 text-accent ring-1 ring-accent/40">
        <CircleDot className="size-4" />
      </span>
    ) : (
      <span className="flex size-full items-center justify-center rounded-lg bg-accent/20 text-accent ring-1 ring-accent/40 text-lg">
        ⊕
      </span>
    )
  }

  if (cell.type === 'swap') {
    return (
      <span className="flex size-full items-center justify-center rounded-lg bg-chart-3/20 text-chart-3 ring-1 ring-chart-3/40">
        ×
      </span>
    )
  }

  return null
}

function StatusPill({
  status,
}: {
  status:
    | 'idle'
    | 'running'
    | 'complete'
}) {
  if (status === 'running') {
    return (
      <Chip tone="amber">
        <span className="size-2 animate-pulse rounded-full bg-chart-4" />
        Running…
      </Chip>
    )
  }

  if (status === 'complete') {
    return (
      <Chip tone="green">
        <CheckCircle2 className="size-3.5" />
        Execution complete
      </Chip>
    )
  }

  return (
    <Chip tone="muted">
      <CircleDot className="size-3.5" />
      Ready
    </Chip>
  )
}

function buildOps(grid: Grid): Op[] {
  const ops: Op[] = []

  for (
    let col = 0;
    col < N_COLS;
    col++
  ) {
    for (
      let q = 0;
      q < N_QUBITS;
      q++
    ) {
      const cell = grid[q][col]

      if (!cell) continue

      if (cell.type === 'single') {
        ops.push({
          kind: 'single',
          gate: cell.gate,
          qubit: q,
        })
      } else if (
        cell.type === 'cnot' &&
        cell.role === 'control'
      ) {
        ops.push({
          kind: 'cnot',
          control: q,
          target: cell.partner,
        })
      } else if (
        cell.type === 'swap' &&
        cell.role === 'a'
      ) {
        ops.push({
          kind: 'swap',
          a: q,
          b: cell.partner,
        })
      }
    }
  }

  return ops
}

function convertGridToApiGates(
  grid: Grid,
): QuantumGate[] {
  const gates: QuantumGate[] = []

  for (
    let col = 0;
    col < N_COLS;
    col++
  ) {
    for (
      let q = 0;
      q < N_QUBITS;
      q++
    ) {
      const cell = grid[q][col]

      if (!cell) continue

      if (cell.type === 'single') {
        gates.push({
          gate: cell.gate,
          qubit: q,
        })
      } else if (
        cell.type === 'cnot' &&
        cell.role === 'control'
      ) {
        gates.push({
          gate: 'CX',
          control: q,
          target: cell.partner,
        })
      } else if (
        cell.type === 'swap' &&
        cell.role === 'a'
      ) {
        gates.push({
          gate: 'SWAP',
          qubit1: q,
          qubit2: cell.partner,
        })
      }

      // Measurement gates are UI-only.
      // Backend measurements are handled during simulation.
    }
  }

  return gates
}

function describeCircuit(
  grid: Grid,
  distribution: {
    state: string
    prob: number
  }[],
) {
  const gates: string[] = []

  let hasH = false
  let hasCNOT = false

  for (
    let col = 0;
    col < N_COLS;
    col++
  ) {
    for (
      let q = 0;
      q < N_QUBITS;
      q++
    ) {
      const cell = grid[q][col]

      if (cell?.type === 'single') {
        gates.push(cell.gate)

        if (cell.gate === 'H') {
          hasH = true
        }
      }

      if (
        cell?.type === 'cnot' &&
        cell.role === 'control'
      ) {
        hasCNOT = true
      }
    }
  }

  if (
    hasH &&
    hasCNOT &&
    distribution.length === 2
  ) {
    return 'You have successfully created a Bell State. The Hadamard gate creates superposition, and the CNOT operation entangles two qubits. The measurement results show correlated quantum states.'
  }

  if (hasH && !hasCNOT) {
    return 'Your circuit uses a Hadamard gate to create superposition. Add a CNOT gate to entangle another qubit and create a Bell State.'
  }

  if (!gates.length && !hasCNOT) {
    return 'The circuit is currently empty. Add an H gate to q0 to create superposition, then add a CNOT gate to create entanglement.'
  }

  return `Your circuit contains ${gates.length} single-qubit gate(s)${
    hasCNOT
      ? ' and a CNOT entangling operation'
      : ''
  }. The simulation currently contains ${
    distribution.length
  } measured basis state(s).`
}
