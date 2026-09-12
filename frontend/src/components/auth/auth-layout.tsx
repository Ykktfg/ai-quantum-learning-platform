
import type { ReactNode } from 'react'
import { Atom, Sparkles, CircuitBoard, Bot } from 'lucide-react'
import { GlassCard } from '@/components/quantum-ui'

const HIGHLIGHTS = [
  { icon: CircuitBoard, label: 'Build circuits in the interactive Quantum Lab' },
  { icon: Bot, label: 'Learn with your personal AI Quantum Copilot' },
  { icon: Sparkles, label: 'Track mastery, streaks & achievements' },
]

/**
 * Full-screen shell for the /login and /signup pages. Reuses the exact
 * QuantumVerse dark/glass aesthetic (grid, gradient orbs, glass card) so the
 * auth screens feel native to the app without touching the main AppShell.
 */
export function AuthLayout({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string
  subtitle: string
  children: ReactNode
  footer: ReactNode
}) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-4 py-10">
      {/* ambient background — matches the app's quantum aesthetic */}
      <div className="pointer-events-none absolute inset-0 bg-grid opacity-60" aria-hidden />
      <div
        className="pointer-events-none absolute -left-32 top-[-10%] size-[420px] rounded-full bg-primary/20 blur-[120px]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -right-24 bottom-[-15%] size-[460px] rounded-full bg-accent/20 blur-[130px]"
        aria-hidden
      />

      <div className="relative z-10 grid w-full max-w-5xl gap-8 lg:grid-cols-2 lg:items-center">
        {/* brand / marketing panel */}
        <section className="hidden flex-col justify-center lg:flex">
          <div className="flex items-center gap-3">
            <span className="relative flex size-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary/25 to-accent/25 ring-1 ring-primary/30">
              <Atom className="size-6 text-primary" style={{ animation: 'orbit-spin 12s linear infinite' }} />
            </span>
            <div className="leading-tight">
              <div className="text-lg font-semibold tracking-tight">
                Quantum<span className="text-primary">Verse</span>
              </div>
              <div className="text-[11px] font-medium tracking-wide text-muted-foreground">AI PLATFORM</div>
            </div>
          </div>

          <h1 className="mt-8 text-balance text-3xl font-bold tracking-tight xl:text-4xl">
            Learn, build & simulate <span className="text-primary text-glow">quantum computing</span>.
          </h1>
          <p className="mt-3 max-w-md text-pretty leading-relaxed text-muted-foreground">
            Your AI-powered path from qubits to algorithms — one interactive lesson at a time.
          </p>

          <ul className="mt-8 space-y-3">
            {HIGHLIGHTS.map(({ icon: Icon, label }) => (
              <li key={label} className="flex items-center gap-3 text-sm text-foreground/85">
                <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
                  <Icon className="size-4" />
                </span>
                {label}
              </li>
            ))}
          </ul>
        </section>

        {/* form card */}
        <GlassCard glow="cyan" className="animate-fade-up p-6 sm:p-8">
          {/* compact brand for small screens */}
          <div className="mb-6 flex items-center gap-3 lg:hidden">
            <span className="relative flex size-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary/25 to-accent/25 ring-1 ring-primary/30">
              <Atom className="size-5 text-primary" />
            </span>
            <div className="leading-tight">
              <div className="font-semibold tracking-tight">
                Quantum<span className="text-primary">Verse</span>
              </div>
              <div className="text-[11px] font-medium tracking-wide text-muted-foreground">AI PLATFORM</div>
            </div>
          </div>

          <h2 className="text-balance text-2xl font-bold tracking-tight">{title}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>

          <div className="mt-6">{children}</div>

          <div className="mt-6 text-center text-sm text-muted-foreground">{footer}</div>
        </GlassCard>
      </div>
    </div>
  )
}
