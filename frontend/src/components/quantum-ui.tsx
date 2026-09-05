import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

export function GlassCard({
  children,
  className,
  glow,
}: {
  children: ReactNode
  className?: string
  glow?: 'cyan' | 'violet' | 'none'
}) {
  return (
    <div
      className={cn(
        'glass rounded-2xl',
        glow === 'cyan' && 'glow-cyan',
        glow === 'violet' && 'glow-violet',
        className,
      )}
    >
      {children}
    </div>
  )
}

export function SectionHeading({
  title,
  subtitle,
  icon,
  action,
}: {
  title: string
  subtitle?: string
  icon?: ReactNode
  action?: ReactNode
}) {
  return (
    <div className="mb-5 flex items-end justify-between gap-4">
      <div className="flex items-center gap-3">
        {icon ? (
          <span className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
            {icon}
          </span>
        ) : null}
        <div>
          <h2 className="text-balance text-lg font-semibold tracking-tight sm:text-xl">{title}</h2>
          {subtitle ? <p className="text-sm text-muted-foreground">{subtitle}</p> : null}
        </div>
      </div>
      {action}
    </div>
  )
}

export function ProgressBar({
  value,
  className,
  tone = 'cyan',
}: {
  value: number
  className?: string
  tone?: 'cyan' | 'violet' | 'green' | 'amber'
}) {
  const toneMap: Record<string, string> = {
    cyan: 'from-primary to-primary/60',
    violet: 'from-accent to-accent/60',
    green: 'from-chart-3 to-chart-3/60',
    amber: 'from-chart-4 to-chart-4/60',
  }
  return (
    <div className={cn('h-2 w-full overflow-hidden rounded-full bg-secondary/60', className)}>
      <div
        className={cn('h-full rounded-full bg-gradient-to-r transition-all duration-700', toneMap[tone])}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  )
}

export function Chip({
  children,
  tone = 'muted',
  className,
}: {
  children: ReactNode
  tone?: 'cyan' | 'violet' | 'green' | 'amber' | 'muted' | 'red'
  className?: string
}) {
  const toneMap: Record<string, string> = {
    cyan: 'bg-primary/12 text-primary ring-primary/25',
    violet: 'bg-accent/15 text-accent ring-accent/30',
    green: 'bg-chart-3/15 text-chart-3 ring-chart-3/30',
    amber: 'bg-chart-4/15 text-chart-4 ring-chart-4/30',
    red: 'bg-destructive/15 text-destructive ring-destructive/30',
    muted: 'bg-secondary/70 text-muted-foreground ring-border',
  }
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium ring-1',
        toneMap[tone],
        className,
      )}
    >
      {children}
    </span>
  )
}

export function RingProgress({
  value,
  size = 132,
  stroke = 10,
  label,
  sublabel,
}: {
  value: number
  size?: number
  stroke?: number
  label?: string
  sublabel?: string
}) {
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const offset = c - (value / 100) * c
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <defs>
          <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="oklch(0.75 0.15 197)" />
            <stop offset="100%" stopColor="oklch(0.62 0.22 300)" />
          </linearGradient>
        </defs>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="oklch(0.7 0.05 260 / 14%)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="url(#ringGrad)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.22,1,0.36,1)' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-bold tracking-tight">{label ?? `${value}%`}</span>
        {sublabel ? <span className="text-xs text-muted-foreground">{sublabel}</span> : null}
      </div>
    </div>
  )
}
