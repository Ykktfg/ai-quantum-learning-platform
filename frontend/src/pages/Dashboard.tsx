import { Link } from 'react-router-dom'
import {
  Flame,
  BookOpenCheck,
  Trophy,
  Gauge,
  Sparkles,
  ArrowRight,
  Atom,
  Zap,
  CircuitBoard,
  Award,
  GraduationCap,
  ChevronRight,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { GlassCard, SectionHeading, ProgressBar, Chip, RingProgress } from '@/components/quantum-ui'
import { WelcomeGreeting } from '@/components/welcome-greeting'
import { student, skillProfile, recentActivity, upcomingChallenges } from '@/lib/data'

const activityIcon = {
  lesson: GraduationCap,
  challenge: Trophy,
  circuit: CircuitBoard,
  badge: Award,
}

export default function DashboardPage() {
  const stats = [
    { label: 'Learning Streak', value: `${student.streak} days`, icon: Flame, tone: 'amber' as const },
    { label: 'Lessons Completed', value: `${student.lessonsCompleted}/${student.totalLessons}`, icon: BookOpenCheck, tone: 'cyan' as const },
    { label: 'Challenges Won', value: `${student.challengesCompleted}/${student.totalChallenges}`, icon: Trophy, tone: 'violet' as const },
    { label: 'Current Level', value: 'Explorer 7', icon: Gauge, tone: 'green' as const },
  ]

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      {/* hero welcome */}
      <GlassCard glow="cyan" className="relative overflow-hidden p-6 sm:p-8 animate-fade-up">
        <div className="absolute -right-10 -top-10 opacity-20">
          <Atom className="size-48 text-primary" style={{ animation: 'orbit-spin 24s linear infinite' }} />
        </div>
        <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-xl">
            <Chip tone="cyan">
              <Sparkles className="size-3.5" />
              Learn → Build → Simulate → Understand
            </Chip>
            <WelcomeGreeting overallProgress={student.overallProgress} />
            <div className="mt-5 flex flex-wrap gap-3">
              <Button className="rounded-xl">
                <Link to="/learn">
                  Continue Learning <ArrowRight className="size-4" />
                </Link>
              </Button>
              <Button variant="secondary" className="rounded-xl">
                <Link to="/lab">
                  Open Circuit Lab <CircuitBoard className="size-4" />
                </Link>
              </Button>
            </div>
          </div>
          <div className="flex items-center justify-center">
            <RingProgress value={student.overallProgress} size={148} sublabel="Overall" />
          </div>
        </div>
      </GlassCard>

      {/* stat cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((s, i) => {
          const Icon = s.icon
          return (
            <GlassCard key={s.label} className="p-4 animate-fade-up sm:p-5" >
              <div className="flex items-center justify-between">
                <span
                  className="flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20"
                  style={{ animationDelay: `${i * 60}ms` }}
                >
                  <Icon className="size-5" />
                </span>
              </div>
              <div className="mt-3 text-2xl font-bold tracking-tight">{s.value}</div>
              <div className="text-sm text-muted-foreground">{s.label}</div>
            </GlassCard>
          )
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* skill profile */}
        <GlassCard className="p-6 lg:col-span-2">
          <SectionHeading
            title="Quantum Skill Profile"
            subtitle="Your mastery across core concepts"
            icon={<Atom className="size-5" />}
          />
          <div className="space-y-5">
            {skillProfile.map((skill) => (
              <div key={skill.name}>
                <div className="mb-1.5 flex items-center justify-between text-sm">
                  <span className="font-medium">{skill.name}</span>
                  <span className="font-mono text-muted-foreground">{skill.value}%</span>
                </div>
                <ProgressBar value={skill.value} tone={skill.tone} />
              </div>
            ))}
          </div>
        </GlassCard>

        {/* AI recommendation */}
        <GlassCard glow="violet" className="flex flex-col p-6">
          <div className="flex items-center gap-2">
            <span className="flex size-9 items-center justify-center rounded-xl bg-accent/15 text-accent ring-1 ring-accent/25">
              <Sparkles className="size-5" />
            </span>
            <div className="font-semibold">AI Recommendation</div>
          </div>
          <p className="mt-4 text-pretty text-sm leading-relaxed text-muted-foreground">
            Based on your performance, we recommend practicing{' '}
            <span className="font-medium text-foreground">Entanglement</span> and{' '}
            <span className="font-medium text-foreground">Controlled Gates</span>. These will unlock the
            Quantum Teleportation challenge.
          </p>
          <div className="mt-4 space-y-2">
            <div className="flex items-center gap-2 rounded-lg bg-secondary/50 px-3 py-2 text-sm">
              <Zap className="size-4 text-accent" /> Entanglement — 48% mastery
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-secondary/50 px-3 py-2 text-sm">
              <CircuitBoard className="size-4 text-accent" /> Controlled Gates
            </div>
          </div>
          <Button variant="secondary" className="mt-4 w-full rounded-xl">
            <Link to="/copilot">
              Ask the AI Copilot <ArrowRight className="size-4" />
            </Link>
          </Button>
        </GlassCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* recent activity */}
        <GlassCard className="p-6 lg:col-span-2">
          <SectionHeading title="Recent Activity" subtitle="Your latest progress" icon={<Gauge className="size-5" />} />
          <ul className="space-y-1">
            {recentActivity.map((a) => {
              const Icon = activityIcon[a.kind]
              return (
                <li
                  key={a.title}
                  className="flex items-center gap-4 rounded-xl px-2 py-3 transition-colors hover:bg-secondary/40"
                >
                  <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
                    <Icon className="size-4" />
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-medium">{a.title}</div>
                    <div className="truncate text-xs text-muted-foreground">{a.meta}</div>
                  </div>
                  <span className="shrink-0 text-xs text-muted-foreground">{a.time}</span>
                </li>
              )
            })}
          </ul>
        </GlassCard>

        {/* upcoming challenges */}
        <GlassCard className="p-6">
          <SectionHeading title="Upcoming Challenges" icon={<Trophy className="size-5" />} />
          <div className="space-y-3">
            {upcomingChallenges.map((c) => (
              <Link
                key={c.title}
                to="/challenges"
                className="group flex items-center gap-3 rounded-xl border border-border bg-secondary/30 p-3 transition-colors hover:border-primary/30 hover:bg-secondary/60"
              >
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-medium">{c.title}</div>
                  <div className="mt-1 flex items-center gap-2">
                    <Chip tone={c.difficulty === 'Hard' ? 'red' : 'amber'}>{c.difficulty}</Chip>
                    <span className="font-mono text-xs text-primary">+{c.xp} XP</span>
                  </div>
                </div>
                <ChevronRight className="size-4 shrink-0 text-muted-foreground transition-transform group-hover:translate-x-0.5" />
              </Link>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  )
}
