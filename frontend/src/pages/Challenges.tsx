import { Link } from 'react-router-dom'
import {
  Trophy,
  Target,
  Lock,
  CheckCircle2,
  Play,
  Award,
  Flame,
  Zap,
} from 'lucide-react'

import { GlassCard, Chip } from '@/components/quantum-ui'
import { challenges, student } from '@/lib/data'

const difficultyTone = {
  Beginner: 'green',
  Intermediate: 'amber',
  Advanced: 'violet',
} as const

const statusMeta = {
  completed: {
    label: 'Completed',
    tone: 'green' as const,
    icon: CheckCircle2,
  },
  'in-progress': {
    label: 'In Progress',
    tone: 'cyan' as const,
    icon: Play,
  },
  available: {
    label: 'Available',
    tone: 'amber' as const,
    icon: Target,
  },
  locked: {
    label: 'Locked',
    tone: 'muted' as const,
    icon: Lock,
  },
}

export default function ChallengesPage() {
  const completed = challenges.filter(
    (c) => c.status === 'completed',
  ).length

  const earnedXp = challenges
    .filter((c) => c.status === 'completed')
    .reduce((sum, c) => sum + c.xp, 0)

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-primary">
          <Trophy className="size-5" />

          <span className="text-sm font-medium tracking-wide">
            GAMIFIED PRACTICE
          </span>
        </div>

        <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">
          Quantum Challenges
        </h1>

        <p className="mt-1 text-muted-foreground">
          Solve real quantum puzzles, earn XP, and unlock achievement badges.
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {[
          {
            label: 'Completed',
            value: `${completed}/${challenges.length}`,
            icon: CheckCircle2,
            tone: 'text-chart-3',
          },
          {
            label: 'XP Earned',
            value: earnedXp.toLocaleString(),
            icon: Zap,
            tone: 'text-primary',
          },
          {
            label: 'Badges',
            value: completed,
            icon: Award,
            tone: 'text-accent',
          },
          {
            label: 'Streak',
            value: `${student.streak} days`,
            icon: Flame,
            tone: 'text-chart-4',
          },
        ].map((stat) => {
          const Icon = stat.icon

          return (
            <GlassCard
              key={stat.label}
              className="flex items-center gap-3 p-4"
            >
              <Icon className={`size-6 ${stat.tone}`} />

              <div>
                <div className="text-xl font-bold tracking-tight">
                  {stat.value}
                </div>

                <div className="text-xs text-muted-foreground">
                  {stat.label}
                </div>
              </div>
            </GlassCard>
          )
        })}
      </div>

      {/* Challenge Grid */}
      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {challenges.map((challenge) => {
          const meta = statusMeta[challenge.status]
          const StatusIcon = meta.icon
          const locked = challenge.status === 'locked'

          return (
            <GlassCard
              key={challenge.id}
              glow={
                challenge.status === 'in-progress'
                  ? 'cyan'
                  : 'none'
              }
              className={`flex flex-col p-5 transition-transform duration-300 ${
                locked
                  ? 'opacity-70'
                  : 'hover:-translate-y-1'
              }`}
            >
              {/* Icon + Status */}
              <div className="flex items-start justify-between gap-3">
                <span className="flex size-11 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 text-primary ring-1 ring-primary/25">
                  <Target className="size-5" />
                </span>

                <Chip tone={meta.tone}>
                  <StatusIcon className="size-3.5" />
                  {meta.label}
                </Chip>
              </div>

              {/* Challenge Title */}
              <h3 className="mt-4 text-balance font-semibold">
                {challenge.title}
              </h3>

              {/* Goal */}
              <p className="mt-1.5 flex-1 text-pretty text-sm text-muted-foreground">
                {challenge.goal}
              </p>

              {/* Difficulty + XP + Badge */}
              <div className="mt-4 flex items-center gap-2">
                <Chip
                  tone={
                    difficultyTone[
                      challenge.difficulty as keyof typeof difficultyTone
                    ]
                  }
                >
                  {challenge.difficulty}
                </Chip>

                <span className="font-mono text-xs text-primary">
                  +{challenge.xp} XP
                </span>

                <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
                  <Award className="size-3.5 text-accent" />
                  {challenge.badge}
                </span>
              </div>

              {/* Action */}
              {locked ? (
                <button
                  type="button"
                  disabled
                  className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-secondary px-4 py-2.5 text-sm font-medium text-muted-foreground"
                >
                  <Lock className="size-4" />
                  Locked
                </button>
              ) : (
                <Link
                  to="/lab"
                  state={{
                    challengeId: challenge.id,
                    challengeTitle: challenge.title,
                  }}
                  className={`mt-4 flex w-full items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-colors ${
                    challenge.status === 'completed'
                      ? 'border border-border bg-secondary text-foreground hover:bg-secondary/80'
                      : 'bg-primary text-primary-foreground hover:bg-primary/90'
                  }`}
                >
                  {challenge.status === 'completed' ? (
                    <>
                      <CheckCircle2 className="size-4" />
                      Solve Again
                    </>
                  ) : (
                    <>
                      <Play className="size-4" />
                      Start Challenge
                    </>
                  )}
                </Link>
              )}
            </GlassCard>
          )
        })}
      </div>
    </div>
  )
}