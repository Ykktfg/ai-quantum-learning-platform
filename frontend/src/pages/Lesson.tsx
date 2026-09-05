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
  const content = lessonContent[currentModule.id] ?? lessonContent.intro

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
            <div className="text-lg font-bold">{currentModule.progress}%</div>
            <div className="text-xs text-muted-foreground">Progress</div>
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
          <h2 className="text-xl font-semibold">Explanation</h2>
        </div>

        <p className="leading-7 text-muted-foreground">
          {content.explanation}
        </p>
      </GlassCard>

      {/* EXAMPLE + VISUAL */}
      <div className="grid gap-6 md:grid-cols-2">
        <GlassCard className="p-6">
          <div className="mb-4 flex items-center gap-2">
            <Lightbulb className="size-5 text-primary" />
            <h2 className="text-xl font-semibold">Example</h2>
          </div>

          <p className="leading-7 text-muted-foreground">
            {content.example}
          </p>
        </GlassCard>

        <GlassCard className="p-6">
          <div className="mb-4 flex items-center gap-2">
            <Play className="size-5 text-primary" />
            <h2 className="text-xl font-semibold">Visual</h2>
          </div>

          <div className="flex min-h-32 items-center justify-center rounded-xl border border-primary/20 bg-primary/5 p-5">
            <pre className="whitespace-pre-wrap text-center font-mono text-sm text-primary">
              {content.visual}
            </pre>
          </div>
        </GlassCard>
      </div>

      {/* QUIZ */}
      <GlassCard className="p-6">
        <div className="mb-5 flex items-center gap-2">
          <Trophy className="size-5 text-primary" />
          <h2 className="text-xl font-semibold">Quick Quiz</h2>
        </div>

        <p className="mb-5 font-medium">{content.question}</p>

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
