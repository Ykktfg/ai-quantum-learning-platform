import { Link } from 'react-router-dom'
import {
  GraduationCap,
  Clock,
  Layers,
  Play,
  CheckCircle2,
  BookOpen,
} from 'lucide-react'

import { GlassCard, Chip, ProgressBar } from '@/components/quantum-ui'
import { modules } from '@/lib/data'

const difficultyTone = {
  Beginner: 'green',
  Intermediate: 'amber',
  Advanced: 'violet',
} as const

export default function LearnPage() {
  const completed = modules.filter((m) => m.progress === 100).length

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-primary">
            <BookOpen className="size-5" />

            <span className="text-sm font-medium tracking-wide">
              LEARNING PATH
            </span>
          </div>

          <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">
            Learn Quantum Computing
          </h1>

          <p className="mt-1 text-muted-foreground">
            Interactive modules that take you from qubits to quantum algorithms.
          </p>
        </div>

        <div className="flex gap-3">
          <div className="rounded-xl border border-border bg-secondary/40 px-4 py-2.5 text-center">
            <div className="text-xl font-bold">
              {completed}
            </div>

            <div className="text-xs text-muted-foreground">
              Completed
            </div>
          </div>

          <div className="rounded-xl border border-border bg-secondary/40 px-4 py-2.5 text-center">
            <div className="text-xl font-bold">
              {modules.length}
            </div>

            <div className="text-xs text-muted-foreground">
              Modules
            </div>
          </div>
        </div>
      </div>

      {/* Module Grid */}
      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {modules.map((m) => {
          const done = m.progress === 100

          return (
            <GlassCard
              key={m.id}
              className="group flex flex-col p-5 transition-transform duration-300 hover:-translate-y-1 hover:glow-cyan"
            >
              {/* Icon and Difficulty */}
              <div className="flex items-start justify-between gap-3">
                <span className="flex size-11 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 text-primary ring-1 ring-primary/25">
                  <GraduationCap className="size-5" />
                </span>

                <Chip
                  tone={
                    difficultyTone[
                      m.difficulty as keyof typeof difficultyTone
                    ]
                  }
                >
                  {m.difficulty}
                </Chip>
              </div>

              {/* Title */}
              <h3 className="mt-4 text-balance font-semibold leading-snug">
                {m.title}
              </h3>

              {/* Description */}
              <p className="mt-1.5 flex-1 text-pretty text-sm text-muted-foreground">
                {m.description}
              </p>

              {/* Time and Lessons */}
              <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
                <span className="flex items-center gap-1.5">
                  <Clock className="size-3.5" />
                  {m.time}
                </span>

                <span className="flex items-center gap-1.5">
                  <Layers className="size-3.5" />
                  {m.lessons} lessons
                </span>
              </div>

              {/* Progress */}
              <div className="mt-3">
                <div className="mb-1.5 flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">
                    Progress
                  </span>

                  <span className="font-mono">
                    {m.progress}%
                  </span>
                </div>

                <ProgressBar
                  value={m.progress}
                  tone={done ? 'green' : 'cyan'}
                />
              </div>

              {/* Open Lesson */}
              <Link
                to="/lesson"
                state={{
                  moduleId: m.id,
                }}
                className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
              >
                {done ? (
                  <>
                    <CheckCircle2 className="size-4" />
                    Review Module
                  </>
                ) : m.progress > 0 ? (
                  <>
                    <Play className="size-4" />
                    Continue Learning
                  </>
                ) : (
                  <>
                    <Play className="size-4" />
                    Start Module
                  </>
                )}
              </Link>
            </GlassCard>
          )
        })}
      </div>
    </div>
  )
}