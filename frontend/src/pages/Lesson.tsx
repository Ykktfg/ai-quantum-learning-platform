import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Lightbulb,
  Play,
  Trophy,
  Atom,
  Zap,
} from 'lucide-react'

import { Button } from '@/components/ui/button'
import { GlassCard, ProgressBar } from '@/components/quantum-ui'
import { modules } from '@/lib/data'

const lessonContent: Record<
  string,
  {
    explanation: string
    example: string
    visual: string
    question: string
    options: string[]
    answer: string
  }
> = {
  intro: {
    explanation:
      'Quantum computing uses quantum-mechanical properties to process information. Instead of classical bits, quantum computers use qubits that can represent quantum states.',
    example:
      'A classical bit is either 0 or 1. A qubit can be prepared in a quantum state that combines the possibilities of 0 and 1.',
    visual: '|0⟩  →  Qubit  →  |0⟩ + |1⟩',
    question: 'What is the basic unit of quantum information?',
    options: ['Bit', 'Qubit', 'Byte', 'Register'],
    answer: 'Qubit',
  },

  qubits: {
    explanation:
      'A qubit is the fundamental unit of quantum information. Its state can be represented using amplitudes, and measurement produces a classical result such as 0 or 1.',
    example:
      'A qubit initialized to |0⟩ has probability 1 of producing 0 when measured.',
    visual: '|ψ⟩ = α|0⟩ + β|1⟩',
    question: 'Which system is used to represent a single quantum bit?',
    options: ['Qubit', 'Pixel', 'Byte', 'Classical register'],
    answer: 'Qubit',
  },

  superposition: {
    explanation:
      'Superposition allows a qubit to exist in a combination of basis states. The Hadamard gate is commonly used to create an equal superposition from |0⟩.',
    example:
      'Applying H to |0⟩ creates an equal superposition, giving approximately 50% probability of measuring 0 and 50% probability of measuring 1.',
    visual: '|0⟩  ── H ──>  (|0⟩ + |1⟩) / √2',
    question: 'Which gate is commonly used to create an equal superposition?',
    options: ['X', 'H', 'Z', 'CNOT'],
    answer: 'H',
  },

  gates: {
    explanation:
      'Quantum gates modify the state of qubits. Single-qubit gates include X, Y, Z, H, S and T, while controlled gates can operate on multiple qubits.',
    example:
      'The X gate flips |0⟩ to |1⟩ and |1⟩ to |0⟩. The H gate creates superposition from a basis state.',
    visual: '|0⟩ ── X ──> |1⟩',
    question: 'Which gate flips |0⟩ to |1⟩?',
    options: ['H', 'X', 'Z', 'S'],
    answer: 'X',
  },

  entanglement: {
    explanation:
      'Entanglement creates correlations between quantum systems. Measuring one part of an entangled system can be strongly correlated with the result of another part.',
    example:
      'A Bell state can be created by applying H to one qubit followed by a CNOT connecting the two qubits.',
    visual: 'q0 ── H ──●──\n             │\nq1 ───────── X──',
    question: 'Which gate is commonly used with H to create a Bell state?',
    options: ['X', 'CNOT', 'T', 'S'],
    answer: 'CNOT',
  },

  circuits: {
    explanation:
      'A quantum circuit is a sequence of quantum gates applied to one or more qubits. Measurements convert quantum information into classical results.',
    example:
      'A simple circuit can apply H to q0 and then measure the qubit.',
    visual: 'q0 ── H ── M ──',
    question: 'What do quantum circuits primarily represent?',
    options: [
      'A sequence of quantum operations',
      'A database table',
      'A network cable',
      'A programming variable',
    ],
    answer: 'A sequence of quantum operations',
  },

  algorithms: {
    explanation:
      'Quantum algorithms use quantum operations to solve particular computational problems. Examples include Grover’s search algorithm and the Quantum Fourier Transform.',
    example:
      'Grover’s algorithm provides a quantum approach to searching an unsorted space using amplitude amplification.',
    visual: 'Input → Quantum Circuit → Measurement → Result',
    question: 'Which is a quantum search algorithm?',
    options: ['Dijkstra', 'Grover', 'Bubble Sort', 'Binary Search'],
    answer: 'Grover',
  },
}

/* -------------------------------------------------------------------------- */
/* VISUAL DEMOS                                                               */
/* -------------------------------------------------------------------------- */

function QuantumVisual({ lessonId }: { lessonId: string }) {
  if (lessonId === 'intro') {
    return (
      <div className="flex w-full flex-col items-center justify-center gap-6 py-4">
        <div className="flex items-center gap-4 sm:gap-8">
          <div className="flex flex-col items-center gap-2">
            <div className="flex size-16 items-center justify-center rounded-2xl border-2 border-primary/40 bg-primary/10 text-2xl font-semibold text-primary shadow-sm">
              0
            </div>
            <span className="text-xs text-muted-foreground">Classical bit</span>
          </div>

          <ArrowRight className="size-6 text-muted-foreground" />

          <div className="relative flex flex-col items-center gap-2">
            <div className="relative flex size-20 items-center justify-center rounded-full border-2 border-primary/50 bg-primary/10 shadow-lg">
              <Atom className="size-10 text-primary animate-pulse" />
            </div>
            <span className="text-xs text-muted-foreground">Qubit</span>
          </div>

          <ArrowRight className="size-6 text-muted-foreground" />

          <div className="flex flex-col items-center gap-2">
            <div className="flex size-16 items-center justify-center rounded-2xl border-2 border-accent/40 bg-accent/10 text-xl font-semibold text-accent">
              0 / 1
            </div>
            <span className="text-xs text-muted-foreground">Quantum state</span>
          </div>
        </div>
      </div>
    )
  }

  if (lessonId === 'qubits') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-3">
        <div className="relative flex size-40 items-center justify-center rounded-full border-2 border-primary/30 bg-gradient-to-br from-primary/10 to-accent/10 shadow-inner">
          <div className="absolute h-32 w-px bg-primary/30" />
          <div className="absolute h-px w-32 bg-primary/30" />

          <div className="absolute left-1/2 top-2 -translate-x-1/2 text-xs font-semibold text-primary">
            |0⟩
          </div>

          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs font-semibold text-accent">
            |1⟩
          </div>

          <div className="absolute size-5 rounded-full bg-primary shadow-lg animate-pulse" />

          <div className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
            Qubit
          </div>
        </div>

        <div className="text-center">
          <div className="font-mono text-sm text-primary">
            |ψ⟩ = α|0⟩ + β|1⟩
          </div>
          <p className="mt-1 text-xs text-muted-foreground">
            A qubit can exist in a combination of states.
          </p>
        </div>
      </div>
    )
  }

  if (lessonId === 'superposition') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-5">
        <div className="flex w-full max-w-md items-center justify-center gap-3 sm:gap-5">
          <div className="flex flex-col items-center gap-2">
            <div className="flex size-14 items-center justify-center rounded-xl border border-border bg-background text-xl font-semibold">
              |0⟩
            </div>
            <span className="text-xs text-muted-foreground">Input</span>
          </div>

          <div className="h-px w-8 bg-border sm:w-12" />

          <div className="relative flex flex-col items-center gap-2">
            <div className="flex size-16 items-center justify-center rounded-xl border-2 border-primary bg-primary/15 text-xl font-bold text-primary shadow-lg animate-pulse">
              H
            </div>
            <span className="text-xs text-primary">Hadamard</span>
          </div>

          <div className="h-px w-8 bg-border sm:w-12" />

          <div className="flex flex-col items-center gap-2">
            <div className="flex size-14 items-center justify-center rounded-xl border border-accent/40 bg-accent/10 text-lg font-semibold text-accent">
              0 + 1
            </div>
            <span className="text-xs text-muted-foreground">Superposition</span>
          </div>
        </div>

        <div className="flex gap-3">
          <div className="rounded-lg border border-primary/20 bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
            50% → 0
          </div>
          <div className="rounded-lg border border-accent/20 bg-accent/10 px-4 py-2 text-sm font-medium text-accent">
            50% → 1
          </div>
        </div>
      </div>
    )
  }

  if (lessonId === 'gates') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-5">
        <div className="flex w-full max-w-md items-center justify-center gap-3 sm:gap-5">
          <div className="flex flex-col items-center gap-2">
            <div className="flex size-14 items-center justify-center rounded-xl border border-border bg-background text-xl font-semibold">
              |0⟩
            </div>
            <span className="text-xs text-muted-foreground">Before</span>
          </div>

          <div className="h-px w-8 bg-border sm:w-12" />

          <div className="relative flex flex-col items-center gap-2">
            <div className="flex size-16 items-center justify-center rounded-xl border-2 border-primary bg-primary/15 text-xl font-bold text-primary shadow-lg animate-pulse">
              X
            </div>
            <span className="text-xs text-primary">NOT gate</span>
          </div>

          <div className="h-px w-8 bg-border sm:w-12" />

          <div className="flex flex-col items-center gap-2">
            <div className="flex size-14 items-center justify-center rounded-xl border border-accent/40 bg-accent/10 text-xl font-semibold text-accent">
              |1⟩
            </div>
            <span className="text-xs text-muted-foreground">After</span>
          </div>
        </div>

        <div className="rounded-lg border border-primary/20 bg-primary/10 px-5 py-2 text-sm font-medium text-primary">
          X flips the qubit: 0 ↔ 1
        </div>
      </div>
    )
  }

  if (lessonId === 'entanglement') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-5">
        <div className="relative w-full max-w-md rounded-xl border border-border bg-background/60 p-5">
          <div className="space-y-8">
            <div className="flex items-center gap-3">
              <span className="w-8 font-mono text-sm text-muted-foreground">
                q0
              </span>

              <div className="flex h-10 flex-1 items-center">
                <div className="h-px flex-1 bg-border" />

                <div className="flex size-12 items-center justify-center rounded-lg border-2 border-primary bg-primary/15 font-bold text-primary animate-pulse">
                  H
                </div>

                <div className="h-px w-8 bg-border" />

                <div className="relative flex size-8 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
                  ●
                </div>

                <div className="h-px flex-1 bg-border" />
              </div>
            </div>

            <div className="absolute left-[calc(50%+38px)] top-[74px] h-8 w-px bg-primary" />

            <div className="flex items-center gap-3">
              <span className="w-8 font-mono text-sm text-muted-foreground">
                q1
              </span>

              <div className="flex h-10 flex-1 items-center">
                <div className="h-px flex-1 bg-border" />

                <div className="flex size-12 items-center justify-center rounded-lg border-2 border-accent bg-accent/15 font-bold text-accent animate-pulse">
                  X
                </div>

                <div className="h-px flex-1 bg-border" />
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-lg border border-accent/20 bg-accent/10 px-4 py-2 text-sm text-accent">
          <Zap className="size-4" />
          q0 and q1 are correlated
        </div>
      </div>
    )
  }

  if (lessonId === 'circuits') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-5">
        <div className="w-full max-w-md rounded-xl border border-border bg-background/60 p-5">
          <div className="flex items-center gap-3">
            <span className="font-mono text-sm text-muted-foreground">
              q0
            </span>

            <div className="flex flex-1 items-center">
              <div className="h-px flex-1 bg-border" />

              <div className="flex size-11 items-center justify-center rounded-lg border-2 border-primary bg-primary/10 font-bold text-primary animate-pulse">
                H
              </div>

              <div className="h-px w-8 bg-border" />

              <div className="flex size-11 items-center justify-center rounded-lg border-2 border-accent bg-accent/10 font-bold text-accent">
                M
              </div>

              <div className="h-px flex-1 bg-border" />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="rounded-lg bg-secondary/70 px-3 py-2 text-xs font-medium">
            Gate
          </span>

          <ArrowRight className="size-4 text-muted-foreground" />

          <span className="rounded-lg bg-secondary/70 px-3 py-2 text-xs font-medium">
            State change
          </span>

          <ArrowRight className="size-4 text-muted-foreground" />

          <span className="rounded-lg bg-secondary/70 px-3 py-2 text-xs font-medium">
            Measurement
          </span>
        </div>
      </div>
    )
  }

  if (lessonId === 'algorithms') {
    return (
      <div className="flex w-full flex-col items-center gap-5 py-5">
        <div className="flex w-full max-w-lg flex-wrap items-center justify-center gap-2">
          {[
            ['1', 'Input'],
            ['2', 'Quantum'],
            ['3', 'Measure'],
            ['4', 'Result'],
          ].map(([number, label], index) => (
            <div key={label} className="flex items-center gap-2">
              <div className="flex flex-col items-center gap-2">
                <div
                  className={`flex size-12 items-center justify-center rounded-xl border font-bold ${
                    index === 1
                      ? 'border-primary bg-primary/15 text-primary animate-pulse'
                      : 'border-border bg-background text-foreground'
                  }`}
                >
                  {number}
                </div>

                <span className="text-xs text-muted-foreground">
                  {label}
                </span>
              </div>

              {index < 3 ? (
                <ArrowRight className="size-4 text-muted-foreground" />
              ) : null}
            </div>
          ))}
        </div>

        <div className="rounded-lg border border-primary/20 bg-primary/10 px-5 py-2 text-sm font-medium text-primary">
          Example: Grover's Search
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-32 items-center justify-center">
      <div className="rounded-xl border border-primary/20 bg-primary/5 px-6 py-4 font-mono text-primary">
        Quantum Circuit
      </div>
    </div>
  )
}

/* -------------------------------------------------------------------------- */
/* LESSON PAGE                                                                */
/* -------------------------------------------------------------------------- */

export default function Lesson() {
  const location = useLocation()
  const navigate = useNavigate()

  const selectedId =
    (location.state as { moduleId?: string } | null)?.moduleId ?? 'intro'

  const currentIndex = Math.max(
    0,
    modules.findIndex((module) => module.id === selectedId),
  )

  const currentModule = modules[currentIndex] ?? modules[0]
  const content =
    lessonContent[currentModule.id] ?? lessonContent.intro

  const [selectedAnswer, setSelectedAnswer] = useState('')
  const [quizCompleted, setQuizCompleted] = useState(false)

  const isCorrect = selectedAnswer === content.answer

  const handleCheckAnswer = () => {
    if (!selectedAnswer) return
    setQuizCompleted(true)
  }

  const handleNext = () => {
    if (currentIndex < modules.length - 1) {
      const nextModule = modules[currentIndex + 1]

      setSelectedAnswer('')
      setQuizCompleted(false)

      navigate('/lesson', {
        state: {
          moduleId: nextModule.id,
        },
      })
    } else {
      navigate('/learn')
    }
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      {/* BACK */}
      <Button
        variant="ghost"
        className="gap-2"
        onClick={() => navigate('/learn')}
      >
        <ArrowLeft className="size-4" />
        Back to Learning
      </Button>

      {/* HEADER */}
      <GlassCard className="p-6">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="flex items-center gap-2 text-primary">
              <BookOpen className="size-5" />

              <span className="text-sm font-medium tracking-wide">
                MODULE {currentIndex + 1} OF {modules.length}
              </span>
            </div>

            <h1 className="mt-2 text-2xl font-bold tracking-tight sm:text-3xl">
              {currentModule.title}
            </h1>

            <p className="mt-2 text-muted-foreground">
              {currentModule.description}
            </p>
          </div>

          <div className="shrink-0 rounded-xl border border-border bg-secondary/40 px-4 py-3 text-center">
            <div className="text-lg font-bold">
              {currentModule.progress}%
            </div>

            <div className="text-xs text-muted-foreground">
              Progress
            </div>
          </div>
        </div>

        <div className="mt-5">
          <ProgressBar
            value={currentModule.progress}
            tone="cyan"
          />
        </div>
      </GlassCard>

      {/* EXPLANATION */}
      <GlassCard className="p-6">
        <div className="mb-4 flex items-center gap-2">
          <BookOpen className="size-5 text-primary" />

          <h2 className="text-xl font-semibold">
            Explanation
          </h2>
        </div>

        <p className="leading-7 text-muted-foreground">
          {content.explanation}
        </p>
      </GlassCard>

      {/* EXAMPLE + VISUAL */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* EXAMPLE */}
        <GlassCard className="p-6">
          <div className="mb-4 flex items-center gap-2">
            <Lightbulb className="size-5 text-primary" />

            <h2 className="text-xl font-semibold">
              Example
            </h2>
          </div>

          <p className="leading-7 text-muted-foreground">
            {content.example}
          </p>
        </GlassCard>

        {/* VISUAL */}
        <GlassCard className="p-6">
          <div className="mb-4 flex items-center gap-2">
            <Play className="size-5 text-primary" />

            <h2 className="text-xl font-semibold">
              Visual
            </h2>
          </div>

          <div className="flex min-h-64 items-center justify-center overflow-hidden rounded-xl border border-primary/20 bg-primary/5 p-5">
            <QuantumVisual lessonId={currentModule.id} />
          </div>
        </GlassCard>
      </div>

      {/* QUIZ */}
      <GlassCard className="p-6">
        <div className="mb-5 flex items-center gap-2">
          <Trophy className="size-5 text-primary" />

          <h2 className="text-xl font-semibold">
            Quick Quiz
          </h2>
        </div>

        <p className="mb-5 font-medium">
          {content.question}
        </p>

        <div className="grid gap-3 sm:grid-cols-2">
          {content.options.map((option) => {
            const selected = selectedAnswer === option

            return (
              <button
                key={option}
                type="button"
                onClick={() => {
                  setSelectedAnswer(option)
                  setQuizCompleted(false)
                }}
                className={[
                  'rounded-xl border p-4 text-left text-sm transition-all',
                  selected
                    ? 'border-primary bg-primary/10 text-primary'
                    : 'border-border bg-secondary/20 hover:border-primary/40 hover:bg-secondary/40',
                ].join(' ')}
              >
                {option}
              </button>
            )
          })}
        </div>

        <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="text-sm">
            {quizCompleted ? (
              isCorrect ? (
                <span className="flex items-center gap-2 text-green-500">
                  <CheckCircle2 className="size-4" />
                  Correct! Great job.
                </span>
              ) : (
                <span className="text-destructive">
                  Not quite. Try the correct concept again.
                </span>
              )
            ) : (
              <span className="text-muted-foreground">
                Select an answer and check it.
              </span>
            )}
          </div>

          <Button
            onClick={handleCheckAnswer}
            disabled={!selectedAnswer}
          >
            Check Answer
          </Button>
        </div>
      </GlassCard>

      {/* NAVIGATION */}
      <div className="flex flex-col gap-3 sm:flex-row sm:justify-between">
        <Button
          variant="secondary"
          disabled={currentIndex === 0}
          onClick={() => {
            const previousModule = modules[currentIndex - 1]

            setSelectedAnswer('')
            setQuizCompleted(false)

            navigate('/lesson', {
              state: {
                moduleId: previousModule.id,
              },
            })
          }}
        >
          <ArrowLeft className="size-4" />
          Previous Lesson
        </Button>

        <Button onClick={handleNext}>
          {currentIndex === modules.length - 1
            ? 'Finish Module'
            : 'Next Lesson'}

          <ArrowRight className="size-4" />
        </Button>
      </div>
    </div>
  )
}