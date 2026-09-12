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
import { formatComplex } from '@/lib/quantum'
import {
  simulateCircuit,
  type QuantumGate,
} from '@/services/quantumApi'
import { cn } from '@/lib/utils'

const N_QUBITS = 3
const N_COLS = 9

/* -------------------------------------------------------------------------- */
/* TYPES                                                                      */
/* -------------------------------------------------------------------------- */

type SingleGateName =
  | 'I'
  | 'H'
  | 'X'
  | 'Y'
  | 'Z'
  | 'S'
  | 'T'
  | 'SX'
  | 'RX'
  | 'RY'
  | 'RZ'

type ControlledGateName =
  | 'CX'
  | 'CY'
  | 'CZ'
  | 'CH'

type Cell =
  | null
  | {
      type: 'single'
      gate: SingleGateName
      angle?: number
    }
  | {
      type: 'controlled'
      gate: ControlledGateName
      role: 'control' | 'target'
      partner: number
    }
  | {
      type: 'swap'
      role: 'a' | 'b'
      partner: number
    }
  | {
      type: 'ccx'
      role: 'control1' | 'control2' | 'target'
      control1: number
      control2: number
      target: number
    }
  | {
      type: 'measure'
    }

type Grid = Cell[][]

type PaletteGate = {
  id: string
  label: string
  full: string
  tone: string
  category:
    | 'single'
    | 'rotation'
    | 'controlled'
    | 'multi'
    | 'utility'
}

type ExtendedQuantumGate = QuantumGate & {
  qubit?: number
  control?: number
  target?: number
  control1?: number
  control2?: number
  angle?: number
}

/*
 * The backend returns a nested simulation response.
 * Keeping this type here prevents the UI from breaking if
 * quantumApi.ts still has the older flat SimulationResult type.
 */
type ComplexAmplitude = {
  real: number
  imag: number
}

type CircuitSimulationResult = {
  simulation: {
    counts: Record<string, number>
    shots: number
    probabilities?: Record<string, number>
  }
  circuit: {
    num_qubits: number
    depth: number
    size: number
  }
  state: {
    statevector: ComplexAmplitude[]
    total_probability: number
    is_normalized: boolean
  }
  measurement: {
    most_likely_state: string
    most_likely_probability: number
  }
  education?: {
    explanation?: string
  }
  circuit_explanation?: unknown
  circuit_diagram?: unknown
}

/* -------------------------------------------------------------------------- */
/* GATE PALETTE                                                               */
/* -------------------------------------------------------------------------- */

const PALETTE: PaletteGate[] = [
  {
    id: 'I',
    label: 'I',
    full: 'Identity — leaves the qubit unchanged',
    tone: 'muted',
    category: 'single',
  },
  {
    id: 'H',
    label: 'H',
    full: 'Hadamard — creates superposition',
    tone: 'primary',
    category: 'single',
  },
  {
    id: 'X',
    label: 'X',
    full: 'Pauli-X — bit flip (NOT)',
    tone: 'primary',
    category: 'single',
  },
  {
    id: 'Y',
    label: 'Y',
    full: 'Pauli-Y — bit and phase flip',
    tone: 'primary',
    category: 'single',
  },
  {
    id: 'Z',
    label: 'Z',
    full: 'Pauli-Z — phase flip',
    tone: 'primary',
    category: 'single',
  },
  {
    id: 'S',
    label: 'S',
    full: 'S Phase gate — π/2 phase rotation',
    tone: 'accent',
    category: 'single',
  },
  {
    id: 'T',
    label: 'T',
    full: 'T gate — π/4 phase rotation',
    tone: 'accent',
    category: 'single',
  },
  {
    id: 'SX',
    label: '√X',
    full: 'SX — square root of the X gate',
    tone: 'accent',
    category: 'single',
  },

  {
    id: 'RX',
    label: 'RX',
    full: 'Rotation around the X axis',
    tone: 'rotation',
    category: 'rotation',
  },
  {
    id: 'RY',
    label: 'RY',
    full: 'Rotation around the Y axis',
    tone: 'rotation',
    category: 'rotation',
  },
  {
    id: 'RZ',
    label: 'RZ',
    full: 'Rotation around the Z axis',
    tone: 'rotation',
    category: 'rotation',
  },

  {
    id: 'CX',
    label: 'CX',
    full: 'Controlled-X / CNOT — applies X when control is |1⟩',
    tone: 'controlled',
    category: 'controlled',
  },
  {
    id: 'CY',
    label: 'CY',
    full: 'Controlled-Y — applies Y when control is |1⟩',
    tone: 'controlled',
    category: 'controlled',
  },
  {
    id: 'CZ',
    label: 'CZ',
    full: 'Controlled-Z — applies Z when control is |1⟩',
    tone: 'controlled',
    category: 'controlled',
  },
  {
    id: 'CH',
    label: 'CH',
    full: 'Controlled-Hadamard — applies H when control is |1⟩',
    tone: 'controlled',
    category: 'controlled',
  },

  {
    id: 'SWAP',
    label: '⇄',
    full: 'SWAP — exchanges the states of two qubits',
    tone: 'green',
    category: 'multi',
  },
  {
    id: 'CCX',
    label: 'CCX',
    full: 'Toffoli — controlled-controlled-X gate',
    tone: 'green',
    category: 'multi',
  },

  {
    id: 'M',
    label: 'M',
    full: 'Measurement — measure the selected qubit',
    tone: 'muted',
    category: 'utility',
  },
]

const SUPPORTED_GATE_COUNT = 17

const rotationGateIds = new Set([
  'RX',
  'RY',
  'RZ',
])

const controlledGateIds = new Set([
  'CX',
  'CY',
  'CZ',
  'CH',
])

const toneClasses: Record<string, string> = {
  primary:
    'bg-primary/15 text-primary ring-primary/40 hover:bg-primary/25',

  accent:
    'bg-accent/15 text-accent ring-accent/40 hover:bg-accent/25',

  rotation:
    'bg-chart-4/15 text-chart-4 ring-chart-4/40 hover:bg-chart-4/25',

  controlled:
    'bg-violet-500/15 text-violet-400 ring-violet-500/40 hover:bg-violet-500/25',

  green:
    'bg-chart-3/15 text-chart-3 ring-chart-3/40 hover:bg-chart-3/25',

  muted:
    'bg-secondary text-muted-foreground ring-border hover:bg-secondary/80',
}

/* -------------------------------------------------------------------------- */
/* GRID                                                                       */
/* -------------------------------------------------------------------------- */

function emptyGrid(): Grid {
  return Array.from(
    { length: N_QUBITS },
    () =>
      Array.from(
        { length: N_COLS },
        () => null as Cell,
      ),
  )
}

function bellGrid(): Grid {
  const g = emptyGrid()

  g[0][0] = {
    type: 'single',
    gate: 'H',
  }

  g[0][2] = {
    type: 'controlled',
    gate: 'CX',
    role: 'control',
    partner: 1,
  }

  g[1][2] = {
    type: 'controlled',
    gate: 'CX',
    role: 'target',
    partner: 0,
  }

  g[0][7] = {
    type: 'measure',
  }

  g[1][7] = {
    type: 'measure',
  }

  return g
}

/* -------------------------------------------------------------------------- */
/* MAIN COMPONENT                                                             */
/* -------------------------------------------------------------------------- */

export function CircuitLab() {
  const [grid, setGrid] = useState<Grid>(bellGrid)
  const [history, setHistory] = useState<Grid[]>([])
  const [selected, setSelected] = useState<string>('H')
  const [rotationAngle, setRotationAngle] =
    useState<number>(Math.PI / 2)

  const [status, setStatus] = useState<
    'idle' | 'running' | 'complete'
  >('idle')

  const [explanation, setExplanation] =
    useState<string | null>(null)

  const [result, setResult] =
    useState<CircuitSimulationResult | null>(null)

  const [error, setError] =
    useState<string | null>(null)

  const operationCount = useMemo(
    () => countOperations(grid),
    [grid],
  )

  const selectedGate = PALETTE.find(
    (gate) => gate.id === selected,
  )

  function pushHistory(next: Grid) {
    setHistory((h) => [
      ...h.slice(-24),
      grid,
    ])

    setGrid(next)
    setStatus('idle')
    setExplanation(null)
    setResult(null)
    setError(null)
  }

  function clearColumnCells(
    next: Grid,
    qubits: number[],
    col: number,
  ) {
    qubits.forEach((qubit) => {
      if (
        qubit >= 0 &&
        qubit < N_QUBITS
      ) {
        removeConnectedGate(
          next,
          qubit,
          col,
        )
      }
    })
  }

  function placeGate(
    q: number,
    col: number,
    gateId: string,
  ) {
    const next = grid.map(
      (row) => row.slice(),
    )

    if (gateId === 'M') {
      removeConnectedGate(
        next,
        q,
        col,
      )

      next[q][col] = {
        type: 'measure',
      }

      pushHistory(next)
      return
    }

    if (controlledGateIds.has(gateId)) {
      if (q + 1 >= N_QUBITS) {
        setError(
          `${gateId} needs two qubits. Place it on q0 or q1.`,
        )
        return
      }

      clearColumnCells(
        next,
        [q, q + 1],
        col,
      )

      const controlledGate =
        gateId as ControlledGateName

      next[q][col] = {
        type: 'controlled',
        gate: controlledGate,
        role: 'control',
        partner: q + 1,
      }

      next[q + 1][col] = {
        type: 'controlled',
        gate: controlledGate,
        role: 'target',
        partner: q,
      }

      pushHistory(next)
      return
    }

    if (gateId === 'SWAP') {
      if (q + 1 >= N_QUBITS) {
        setError(
          'SWAP needs two qubits. Place it on q0 or q1.',
        )
        return
      }

      clearColumnCells(
        next,
        [q, q + 1],
        col,
      )

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

      pushHistory(next)
      return
    }

    if (gateId === 'CCX') {
      if (q !== 0) {
        setError(
          'CCX uses all three qubits. Place it on q0: q0 and q1 become controls, and q2 becomes the target.',
        )
        return
      }

      clearColumnCells(
        next,
        [0, 1, 2],
        col,
      )

      next[0][col] = {
        type: 'ccx',
        role: 'control1',
        control1: 0,
        control2: 1,
        target: 2,
      }

      next[1][col] = {
        type: 'ccx',
        role: 'control2',
        control1: 0,
        control2: 1,
        target: 2,
      }

      next[2][col] = {
        type: 'ccx',
        role: 'target',
        control1: 0,
        control2: 1,
        target: 2,
      }

      pushHistory(next)
      return
    }

    removeConnectedGate(
      next,
      q,
      col,
    )

    next[q][col] = {
      type: 'single',
      gate: gateId as SingleGateName,
      ...(rotationGateIds.has(gateId)
        ? {
            angle: rotationAngle,
          }
        : {}),
    }

    pushHistory(next)
  }

  function clearCell(
    q: number,
    col: number,
  ) {
    const cell = grid[q][col]

    if (!cell) return

    const next = grid.map(
      (row) => row.slice(),
    )

    removeConnectedGate(
      next,
      q,
      col,
    )

    pushHistory(next)
  }

  async function run() {
    try {
      setStatus('running')
      setError(null)
      setExplanation(null)

      const gates =
        convertGridToApiGates(grid)

      const response =
        await simulateCircuit({
          qubits: N_QUBITS,
          gates,
          shots: 1000,
        })

      /*
       * quantumApi.ts currently exposes an older flat
       * SimulationResult type, while the backend returns
       * the nested structure used by this UI.
       */
      setResult(
        response as unknown as CircuitSimulationResult,
      )

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

    const prev =
      history[history.length - 1]

    setHistory((h) =>
      h.slice(0, -1),
    )

    setGrid(prev)
    setStatus('idle')
    setResult(null)
    setExplanation(null)
    setError(null)
  }

  function explain() {
    const distribution = result
      ? Object.entries(
          result.simulation.counts,
        ).map(
          ([state, count]) => ({
            state,
            prob:
              result.simulation.shots > 0
                ? count /
                  result.simulation.shots
                : 0,
          }),
        )
      : []

    setExplanation(
      describeCircuit(
        grid,
        distribution,
      ),
    )
  }

  function optimize() {
    setExplanation(
      'Optimization: look for redundant gate pairs and unnecessary operations. Self-inverse pairs such as H·H, X·X, Y·Y, Z·Z, CX·CX and SWAP·SWAP can often be cancelled when applied consecutively to the same qubits.',
    )
  }

  const measuredQubits = grid
    .map((row, q) =>
      row.some(
        (cell) =>
          cell?.type === 'measure',
      )
        ? q
        : -1,
    )
    .filter((q) => q >= 0)

  return (
    <div className="space-y-6">

      {/* MAIN LAB */}
      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">

        {/* GATE PALETTE */}
        <GlassCard className="h-fit p-4">
          <div className="mb-1 flex items-center gap-2 text-sm font-semibold">
            <CircuitBoard className="size-4 text-primary" />
            Quantum Gates
          </div>

          <div className="mb-4 text-xs text-muted-foreground">
            {SUPPORTED_GATE_COUNT} supported quantum gates
          </div>

          <PaletteSection
            title="Single Qubit"
            gates={PALETTE.filter(
              (g) =>
                g.category === 'single',
            )}
            selected={selected}
            setSelected={setSelected}
          />

          <PaletteSection
            title="Rotation"
            gates={PALETTE.filter(
              (g) =>
                g.category === 'rotation',
            )}
            selected={selected}
            setSelected={setSelected}
          />

          {/* ROTATION ANGLE */}
          {rotationGateIds.has(
            selected,
          ) ? (
            <div className="mb-4 rounded-xl border border-chart-4/25 bg-chart-4/5 p-3">
              <div className="mb-2 flex items-center justify-between">
                <span className="text-xs font-medium">
                  Rotation angle
                </span>

                <span className="font-mono text-xs text-chart-4">
                  {rotationAngle.toFixed(3)} rad
                </span>
              </div>

              <input
                type="range"
                min={-Math.PI * 2}
                max={Math.PI * 2}
                step={0.01}
                value={rotationAngle}
                onChange={(e) =>
                  setRotationAngle(
                    Number(
                      e.target.value,
                    ),
                  )
                }
                className="w-full"
              />

              <div className="mt-2 grid grid-cols-3 gap-1">
                <button
                  type="button"
                  onClick={() =>
                    setRotationAngle(
                      Math.PI / 4,
                    )
                  }
                  className="rounded-md bg-secondary/70 px-2 py-1 text-[10px] hover:bg-secondary"
                >
                  π/4
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setRotationAngle(
                      Math.PI / 2,
                    )
                  }
                  className="rounded-md bg-secondary/70 px-2 py-1 text-[10px] hover:bg-secondary"
                >
                  π/2
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setRotationAngle(
                      Math.PI,
                    )
                  }
                  className="rounded-md bg-secondary/70 px-2 py-1 text-[10px] hover:bg-secondary"
                >
                  π
                </button>
              </div>
            </div>
          ) : null}

          <PaletteSection
            title="Controlled"
            gates={PALETTE.filter(
              (g) =>
                g.category ===
                'controlled',
            )}
            selected={selected}
            setSelected={setSelected}
          />

          <PaletteSection
            title="Multi-Qubit"
            gates={PALETTE.filter(
              (g) =>
                g.category === 'multi',
            )}
            selected={selected}
            setSelected={setSelected}
          />

          <PaletteSection
            title="Measurement"
            gates={PALETTE.filter(
              (g) =>
                g.category === 'utility',
            )}
            selected={selected}
            setSelected={setSelected}
          />

          <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
            Select a gate and click a timeline slot, or drag the gate onto a qubit line.
          </p>

          <div className="mt-3 rounded-lg bg-secondary/50 p-2.5 text-xs">
            <div className="font-medium text-foreground">
              {selectedGate?.label}{' '}
              {selected === 'M'
                ? 'tool'
                : 'gate'}
            </div>

            <div className="mt-0.5 text-muted-foreground">
              {selectedGate?.full}
            </div>

            {rotationGateIds.has(
              selected,
            ) ? (
              <div className="mt-1 font-mono text-chart-4">
                θ = {rotationAngle.toFixed(3)} radians
              </div>
            ) : null}
          </div>
        </GlassCard>

        {/* CIRCUIT WORKSPACE */}
        <GlassCard className="overflow-hidden p-0">

          {/* CONTROLS */}
          <div className="flex flex-wrap items-center gap-2 border-b border-border p-3">

            <Button
              size="sm"
              className="rounded-lg"
              onClick={run}
              disabled={
                status === 'running'
              }
            >
              <Play className="size-4" />

              {status === 'running'
                ? 'Running...'
                : 'Run Circuit'}
            </Button>

            <Button
              size="sm"
              variant="secondary"
              className="rounded-lg"
              onClick={() =>
                pushHistory(
                  bellGrid(),
                )
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
                pushHistory(
                  emptyGrid(),
                )
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
              disabled={
                !history.length
              }
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
                      }).map(
                        (_, col) => (
                          <CellSlot
                            key={col}
                            cell={
                              grid[q][col]
                            }
                            onPlace={(
                              gateId,
                            ) =>
                              placeGate(
                                q,
                                col,
                                gateId,
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
                                ? clearCell(
                                    q,
                                    col,
                                  )
                                : placeGate(
                                    q,
                                    col,
                                    selected,
                                  )
                            }
                          />
                        ),
                      )}
                    </div>
                  </div>
                </div>
              ))}

            </div>
          </div>

          {/* STATUS */}
          <div className="flex items-center gap-3 border-t border-border px-4 py-2.5 text-sm">
            <StatusPill
              status={status}
            />

            <span className="text-muted-foreground">
              {operationCount}{' '}
              operation
              {operationCount === 1
                ? ''
                : 's'}{' '}
              · {N_QUBITS} qubits
            </span>

            {measuredQubits.length ? (
              <span className="ml-auto font-mono text-xs text-muted-foreground">
                measuring q
                {measuredQubits.join(
                  ', q',
                )}
              </span>
            ) : null}
          </div>
        </GlassCard>
      </div>

      {/* ERROR */}
      {error ? (
        <GlassCard className="border border-destructive/30 p-4">
          <p className="text-sm text-destructive">
            {error}
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
        <>
          <div className="grid gap-6 lg:grid-cols-3">

            {/* MEASUREMENT RESULTS */}
            <GlassCard className="p-5">
              <div className="mb-4 flex items-center gap-2 font-semibold">
                <Activity className="size-4 text-primary" />
                Measurement Results
              </div>

              <div className="space-y-3">
                {Object.entries(
                  result.simulation.counts,
                )
                  .sort(
                    ([, a], [, b]) =>
                      b - a,
                  )
                  .map(
                    ([state, count]) => {
                      const percentage =
                        result.simulation.shots >
                        0
                          ? (count /
                              result
                                .simulation
                                .shots) *
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
                              {percentage.toFixed(
                                1,
                              )}
                              %
                            </span>
                          </div>

                          <div className="h-2.5 overflow-hidden rounded-full bg-secondary/60">
                            <div
                              className="h-full rounded-full bg-primary transition-all duration-700"
                              style={{
                                width: `${percentage}%`,
                              }}
                            />
                          </div>
                        </div>
                      )
                    },
                  )}
              </div>
            </GlassCard>

            {/* PROBABILITY DISTRIBUTION */}
            <GlassCard className="p-5">
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2 font-semibold">
                  <BarChart3 className="size-4 text-primary" />
                  Probability Distribution
                </div>

                <span className="text-xs text-muted-foreground">
                  {result.simulation.shots} shots
                </span>
              </div>

              <ProbabilityChart
                result={result}
              />
            </GlassCard>

            {/* STATE VECTOR */}
            <GlassCard className="p-5">
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2 font-semibold">
                  <Sigma className="size-4 text-primary" />
                  State Vector
                </div>

                <Chip tone="cyan">
                  {
                    result.state.statevector
                      .length
                  } amplitudes
                </Chip>
              </div>

              <div className="max-h-64 space-y-2 overflow-y-auto pr-1">
                {result.state.statevector.map(
                  (amp, i) => {
                    const probability =
                      amp.real *
                        amp.real +
                      amp.imag *
                        amp.imag

                    const magnitude =
                      Math.sqrt(
                        probability,
                      )

                    const active =
                      probability >
                      1e-9

                    const basisState =
                      i
                        .toString(2)
                        .padStart(
                          result.circuit
                            .num_qubits,
                          '0',
                        )

                    return (
                      <div
                        key={i}
                        className={cn(
                          'rounded-lg border p-2.5 transition-all',
                          active
                            ? 'border-primary/30 bg-primary/10'
                            : 'border-border/40 bg-secondary/20',
                        )}
                      >
                        <div className="mb-1.5 flex items-center justify-between gap-2">
                          <span className="font-mono text-xs font-semibold">
                            |{basisState}⟩
                          </span>

                          <span className="font-mono text-[11px] text-muted-foreground">
                            {formatComplex({
                              re: amp.real,
                              im: amp.imag,
                            })}
                          </span>
                        </div>

                        <div className="flex items-center gap-2">
                          <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-secondary">
                            <div
                              className="h-full rounded-full bg-primary transition-all duration-700"
                              style={{
                                width: `${Math.min(
                                  magnitude *
                                    100,
                                  100,
                                )}%`,
                              }}
                            />
                          </div>

                          <span className="w-14 text-right text-[10px] text-muted-foreground">
                            {(
                              probability *
                              100
                            ).toFixed(
                              1,
                            )}
                            %
                          </span>
                        </div>
                      </div>
                    )
                  },
                )}
              </div>

              <div className="mt-3 flex items-center justify-between border-t border-border pt-3 text-xs text-muted-foreground">
                <span>
                  Total probability
                </span>

                <span className="font-mono text-primary">
                  {result.state.total_probability.toFixed(
                    4,
                  )}
                </span>
              </div>
            </GlassCard>
          </div>

          {/* EXTRA QUANTUM INSIGHT */}
          <GlassCard className="p-5">
            <div className="mb-4 flex items-center gap-2 font-semibold">
              <Activity className="size-4 text-primary" />
              Quantum State Analysis
            </div>

            <div className="grid gap-3 md:grid-cols-3">

              <div className="rounded-xl bg-secondary/50 p-4">
                <div className="text-xs text-muted-foreground">
                  Most Likely State
                </div>

                <div className="mt-1 font-mono text-lg font-semibold text-primary">
                  |{
                    result.measurement
                      .most_likely_state
                  }⟩
                </div>
              </div>

              <div className="rounded-xl bg-secondary/50 p-4">
                <div className="text-xs text-muted-foreground">
                  Probability
                </div>

                <div className="mt-1 text-lg font-semibold">
                  {(
                    result.measurement
                      .most_likely_probability *
                    100
                  ).toFixed(1)}
                  %
                </div>
              </div>

              <div className="rounded-xl bg-secondary/50 p-4">
                <div className="text-xs text-muted-foreground">
                  Normalized
                </div>

                <div className="mt-1 flex items-center gap-2 text-lg font-semibold">
                  <CheckCircle2 className="size-4 text-primary" />

                  {result.state
                    .is_normalized
                    ? 'Yes'
                    : 'No'}
                </div>
              </div>

            </div>

            {result.education?.explanation ? (
              <div className="mt-4 rounded-xl border border-primary/20 bg-primary/5 p-4">
                <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-primary">
                  What this means
                </div>

                <p className="text-sm leading-relaxed text-muted-foreground">
                  {
                    result.education
                      .explanation
                  }
                </p>
              </div>
            ) : null}
          </GlassCard>
        </>
      )}

      {/* CIRCUIT STATISTICS */}
      {result && (
        <GlassCard className="p-5">
          <div className="mb-4 flex items-center gap-2 font-semibold">
            <CircuitBoard className="size-4 text-primary" />
            Circuit Statistics
          </div>

          <div className="grid gap-3 sm:grid-cols-4">

            <StatCard
              label="Qubits"
              value={
                result.circuit
                  .num_qubits
              }
            />

            <StatCard
              label="Shots"
              value={
                result.simulation
                  .shots
              }
            />

            <StatCard
              label="Depth"
              value={
                result.circuit
                  .depth
              }
            />

            <StatCard
              label="Gates"
              value={
                result.circuit
                  .size
              }
            />

          </div>
        </GlassCard>
      )}
    </div>
  )
}

/* -------------------------------------------------------------------------- */
/* PROBABILITY CHART                                                          */
/* -------------------------------------------------------------------------- */

function ProbabilityChart({
  result,
}: {
  result: CircuitSimulationResult
}) {
  const probabilities =
    result.simulation
      .probabilities &&
    Object.keys(
      result.simulation
        .probabilities,
    ).length > 0
      ? result.simulation
          .probabilities
      : Object.fromEntries(
          Object.entries(
            result.simulation
              .counts,
          ).map(
            ([state, count]) => [
              state,
              result.simulation
                .shots > 0
                ? count /
                  result
                    .simulation
                    .shots
                : 0,
            ],
          ),
        )

  const entries = Object.entries(
    probabilities,
  )
    .sort(
      ([, a], [, b]) => b - a,
    )
    .slice(0, 8)

  const maxProbability =
    Math.max(
      ...entries.map(
        ([, probability]) =>
          probability,
      ),
      0.01,
    )

  return (
    <div className="space-y-3">

      <div className="flex h-56 items-end gap-2 border-b border-border px-1 pb-2">
        {entries.map(
          ([state, probability]) => {
            const percentage =
              probability * 100

            const height =
              (probability /
                maxProbability) *
              100

            return (
              <div
                key={state}
                className="flex h-full min-w-0 flex-1 flex-col items-center justify-end gap-1.5"
              >
                <span className="text-[10px] font-semibold text-primary">
                  {percentage.toFixed(
                    1,
                  )}
                  %
                </span>

                <div className="flex h-[78%] w-full items-end justify-center">
                  <div
                    className="w-full max-w-10 rounded-t-lg bg-primary/80 transition-all duration-700 hover:bg-primary"
                    style={{
                      height: `${Math.max(
                        height,
                        3,
                      )}%`,
                    }}
                    title={`|${state}⟩ — ${percentage.toFixed(
                      2,
                    )}%`}
                  />
                </div>

                <span className="max-w-full truncate font-mono text-[10px] text-muted-foreground">
                  |{state}⟩
                </span>
              </div>
            )
          },
        )}
      </div>

      <div className="flex items-center justify-between text-[10px] text-muted-foreground">
        <span>
          Measurement probability
        </span>

        <span>
          Highest:{' '}
          {(
            maxProbability * 100
          ).toFixed(1)}
          %
        </span>
      </div>
    </div>
  )
}

/* -------------------------------------------------------------------------- */
/* STAT CARD                                                                  */
/* -------------------------------------------------------------------------- */

function StatCard({
  label,
  value,
}: {
  label: string
  value: number
}) {
  return (
    <div className="rounded-lg bg-secondary/50 p-3">
      <div className="text-xs text-muted-foreground">
        {label}
      </div>

      <div className="mt-1 text-lg font-semibold">
        {value}
      </div>
    </div>
  )
}

/* -------------------------------------------------------------------------- */
/* PALETTE SECTION                                                            */
/* -------------------------------------------------------------------------- */

function PaletteSection({
  title,
  gates,
  selected,
  setSelected,
}: {
  title: string
  gates: PaletteGate[]
  selected: string
  setSelected: (
    gate: string,
  ) => void
}) {
  return (
    <div className="mb-4">
      <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </div>

      <div className="grid grid-cols-4 gap-2">
        {gates.map(
          (gate) => (
            <button
              key={gate.id}
              type="button"
              draggable
              onDragStart={(e) =>
                e.dataTransfer.setData(
                  'gate',
                  gate.id,
                )
              }
              onClick={() =>
                setSelected(
                  gate.id,
                )
              }
              title={gate.full}
              className={cn(
                'flex aspect-square min-h-12 flex-col items-center justify-center rounded-xl px-1 font-mono text-sm font-bold ring-1 transition-all',
                toneClasses[
                  gate.tone
                ],
                selected ===
                  gate.id &&
                  'scale-105 ring-2 ring-offset-2 ring-offset-card',
              )}
            >
              {gate.label}
            </button>
          ),
        )}
      </div>
    </div>
  )
}

/* -------------------------------------------------------------------------- */
/* CELL                                                                       */
/* -------------------------------------------------------------------------- */

function CellSlot({
  cell,
  onPlace,
  onClear,
  onClick,
}: {
  cell: Cell
  onPlace: (
    gate: string,
  ) => void
  onClear: () => void
  onClick: () => void
}) {
  const [over, setOver] =
    useState(false)

  return (
    <button
      type="button"
      onClick={onClick}
      onDoubleClick={onClear}
      onDragOver={(e) => {
        e.preventDefault()
        setOver(true)
      }}
      onDragLeave={() =>
        setOver(false)
      }
      onDrop={(e) => {
        e.preventDefault()
        setOver(false)

        const gateId =
          e.dataTransfer.getData(
            'gate',
          )

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
      <CellContent
        cell={cell}
      />
    </button>
  )
}

function CellContent({
  cell,
}: {
  cell: Cell
}) {
  if (!cell) {
    return <span>+</span>
  }

  if (cell.type === 'single') {
    return (
      <span
        className={cn(
          'flex size-full flex-col items-center justify-center rounded-lg ring-1',
          rotationGateIds.has(
            cell.gate,
          )
            ? 'bg-chart-4/20 text-chart-4 ring-chart-4/40'
            : 'bg-primary/20 text-primary ring-primary/40',
        )}
      >
        <span>
          {cell.gate}
        </span>

        {cell.angle !==
        undefined ? (
          <span className="text-[8px] font-normal">
            {cell.angle.toFixed(
              2,
            )}
          </span>
        ) : null}
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

  if (
    cell.type ===
    'controlled'
  ) {
    if (
      cell.role ===
      'control'
    ) {
      return (
        <span className="flex size-full flex-col items-center justify-center rounded-lg bg-violet-500/20 text-violet-400 ring-1 ring-violet-500/40">
          <CircleDot className="size-4" />

          <span className="text-[8px]">
            {cell.gate}
          </span>
        </span>
      )
    }

    return (
      <span className="flex size-full items-center justify-center rounded-lg bg-violet-500/20 text-violet-400 ring-1 ring-violet-500/40">
        {cell.gate ===
        'CX'
          ? '⊕'
          : cell.gate.replace(
              'C',
              '',
            )}
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

  if (cell.type === 'ccx') {
    if (
      cell.role ===
        'control1' ||
      cell.role ===
        'control2'
    ) {
      return (
        <span className="flex size-full flex-col items-center justify-center rounded-lg bg-chart-3/20 text-chart-3 ring-1 ring-chart-3/40">
          <CircleDot className="size-4" />

          <span className="text-[8px]">
            CCX
          </span>
        </span>
      )
    }

    return (
      <span className="flex size-full items-center justify-center rounded-lg bg-chart-3/20 text-chart-3 ring-1 ring-chart-3/40 text-lg">
        ⊕
      </span>
    )
  }

  return null
}

/* -------------------------------------------------------------------------- */
/* STATUS                                                                     */
/* -------------------------------------------------------------------------- */

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

/* -------------------------------------------------------------------------- */
/* GRID HELPERS                                                               */
/* -------------------------------------------------------------------------- */

function removeConnectedGate(
  grid: Grid,
  q: number,
  col: number,
) {
  const cell = grid[q][col]

  if (!cell) {
    grid[q][col] = null
    return
  }

  if (
    cell.type ===
    'controlled'
  ) {
    grid[q][col] = null

    if (
      cell.partner >= 0 &&
      cell.partner <
        N_QUBITS
    ) {
      grid[cell.partner][
        col
      ] = null
    }

    return
  }

  if (cell.type === 'swap') {
    grid[q][col] = null

    if (
      cell.partner >= 0 &&
      cell.partner <
        N_QUBITS
    ) {
      grid[cell.partner][
        col
      ] = null
    }

    return
  }

  if (cell.type === 'ccx') {
    grid[0][col] = null
    grid[1][col] = null
    grid[2][col] = null

    return
  }

  grid[q][col] = null
}

function countOperations(
  grid: Grid,
) {
  let count = 0

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
      const cell =
        grid[q][col]

      if (!cell) continue

      if (
        cell.type ===
          'single' ||
        cell.type ===
          'measure'
      ) {
        count += 1
      } else if (
        cell.type ===
          'controlled' &&
        cell.role ===
          'control'
      ) {
        count += 1
      } else if (
        cell.type ===
          'swap' &&
        cell.role === 'a'
      ) {
        count += 1
      } else if (
        cell.type ===
          'ccx' &&
        cell.role ===
          'control1'
      ) {
        count += 1
      }
    }
  }

  return count
}

/* -------------------------------------------------------------------------- */
/* BACKEND CONVERSION                                                         */
/* -------------------------------------------------------------------------- */

function convertGridToApiGates(
  grid: Grid,
): ExtendedQuantumGate[] {
  const gates: ExtendedQuantumGate[] =
    []

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
      const cell =
        grid[q][col]

      if (!cell) continue

      if (
        cell.type ===
        'single'
      ) {
        gates.push({
          gate: cell.gate,
          qubit: q,

          ...(cell.angle !==
          undefined
            ? {
                angle:
                  cell.angle,
              }
            : {}),
        })

        continue
      }

      if (
        cell.type ===
          'controlled' &&
        cell.role ===
          'control'
      ) {
        gates.push({
          gate: cell.gate,
          control: q,
          target:
            cell.partner,
        })

        continue
      }

      if (
        cell.type === 'swap' &&
        cell.role === 'a'
      ) {
        gates.push({
          gate: 'SWAP',
          control: q,
          target:
            cell.partner,
        })

        continue
      }

      if (
        cell.type === 'ccx' &&
        cell.role ===
          'control1'
      ) {
        gates.push({
          gate: 'CCX',
          control1:
            cell.control1,
          control2:
            cell.control2,
          target:
            cell.target,
        })

        continue
      }

      /*
       * Measurement is not sent to the backend.
       * The simulator performs measurement
       * using the requested number of shots.
       */
    }
  }

  return gates
}

/* -------------------------------------------------------------------------- */
/* CIRCUIT EXPLANATION                                                        */
/* -------------------------------------------------------------------------- */

function describeCircuit(
  grid: Grid,
  distribution: {
    state: string
    prob: number
  }[],
) {
  const gates: string[] = []

  let hasH = false
  let hasEntanglingGate =
    false

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
      const cell =
        grid[q][col]

      if (
        cell?.type ===
        'single'
      ) {
        gates.push(
          cell.gate,
        )

        if (
          cell.gate === 'H'
        ) {
          hasH = true
        }
      }

      if (
        cell?.type ===
          'controlled' &&
        cell.role ===
          'control'
      ) {
        gates.push(
          cell.gate,
        )

        hasEntanglingGate =
          true
      }

      if (
        cell?.type === 'swap' &&
        cell.role === 'a'
      ) {
        gates.push('SWAP')
      }

      if (
        cell?.type === 'ccx' &&
        cell.role ===
          'control1'
      ) {
        gates.push('CCX')
        hasEntanglingGate =
          true
      }
    }
  }

  const hasCX =
    gates.includes('CX')

  if (
    hasH &&
    hasCX &&
    distribution.length === 2
  ) {
    return 'You have created a Bell-style entangling circuit. The Hadamard gate creates superposition and the CX gate correlates the target qubit with the control qubit. The measurement distribution can then reveal the correlated basis states.'
  }

  if (
    hasH &&
    !hasEntanglingGate
  ) {
    return 'Your circuit contains a Hadamard gate, so at least one qubit can enter superposition. To explore entanglement, add a controlled gate such as CX, CY, CZ or CH between two qubits.'
  }

  if (!gates.length) {
    return 'The circuit currently contains no quantum gates. Select one of the 17 supported gates from the palette and place it on the circuit timeline.'
  }

  const uniqueGates = [
    ...new Set(gates),
  ]

  return `Your circuit contains ${gates.length} quantum operation${
    gates.length === 1
      ? ''
      : 's'
  } using ${uniqueGates.join(
    ', ',
  )}. ${
    hasEntanglingGate
      ? 'It contains a multi-qubit controlled operation that can create or manipulate correlations between qubits.'
      : 'The current gates operate without a controlled entangling operation.'
  } The simulation contains ${
    distribution.length
  } measured basis state${
    distribution.length === 1
      ? ''
      : 's'
  }.`
}