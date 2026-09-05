import { Award, Lock } from 'lucide-react'
import { EmptyState } from '@/components/analytics/empty-state'
import { resolveIcon } from '@/components/analytics/icon-map'
import type { Achievement } from '@/types/user'
import { cn } from '@/lib/utils'

export function AchievementGrid({ achievements }: { achievements: Achievement[] }) {
  if (achievements.length === 0) {
    return (
      <EmptyState
        icon={Award}
        title="No achievements yet"
        description="Complete lessons and challenges to start unlocking badges."
      />
    )
  }

  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      {achievements.map((b) => {
        const Icon = resolveIcon(b.icon)
        return (
          <div
            key={b.id}
            className={cn(
              'flex flex-col items-center rounded-2xl border p-5 text-center transition-transform',
              b.earned
                ? 'border-primary/25 bg-gradient-to-b from-primary/10 to-transparent hover:-translate-y-1'
                : 'border-border bg-secondary/20',
            )}
          >
            <span
              className={cn(
                'flex size-14 items-center justify-center rounded-2xl ring-1',
                b.earned
                  ? 'bg-primary/15 text-primary ring-primary/30 glow-cyan'
                  : 'bg-secondary text-muted-foreground ring-border',
              )}
            >
              {b.earned ? <Icon className="size-7" /> : <Lock className="size-6" />}
            </span>
            <div className={cn('mt-3 text-sm font-semibold', !b.earned && 'text-muted-foreground')}>{b.name}</div>
            <div className="mt-1 text-xs text-muted-foreground">{b.description}</div>

            {/* optional progress toward a locked badge */}
            {!b.earned && typeof b.progress === 'number' ? (
              <div className="mt-3 w-full">
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-secondary/60">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-accent to-accent/60"
                    style={{ width: `${Math.min(100, Math.max(0, b.progress))}%` }}
                  />
                </div>
                <div className="mt-1 font-mono text-[11px] text-muted-foreground">{b.progress}%</div>
              </div>
            ) : null}
          </div>
        )
      })}
    </div>
  )
}
