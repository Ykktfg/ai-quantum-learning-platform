import { BookOpenCheck, Trophy, CircuitBoard, Award, History } from 'lucide-react'
import { EmptyState } from '@/components/analytics/empty-state'
import type { ActivityKind, LearningActivity } from '@/types/user'
import { cn } from '@/lib/utils'

const KIND_META: Record<ActivityKind, { icon: typeof BookOpenCheck; tone: string }> = {
  lesson: { icon: BookOpenCheck, tone: 'bg-primary/12 text-primary ring-primary/25' },
  challenge: { icon: Trophy, tone: 'bg-chart-4/15 text-chart-4 ring-chart-4/30' },
  circuit: { icon: CircuitBoard, tone: 'bg-chart-3/15 text-chart-3 ring-chart-3/30' },
  badge: { icon: Award, tone: 'bg-accent/15 text-accent ring-accent/30' },
}

export function ActivityTimeline({ activity }: { activity: LearningActivity[] }) {
  if (activity.length === 0) {
    return (
      <EmptyState
        icon={History}
        title="No recent activity"
        description="Your completed lessons, challenges and circuits will show up here."
      />
    )
  }

  return (
    <ul className="space-y-2">
      {activity.map((item) => {
        const meta = KIND_META[item.kind]
        const Icon = meta.icon
        return (
          <li
            key={item.id}
            className="flex items-center gap-3 rounded-xl border border-border bg-secondary/30 p-3"
          >
            <span className={cn('flex size-9 shrink-0 items-center justify-center rounded-lg ring-1', meta.tone)}>
              <Icon className="size-4" />
            </span>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium">{item.title}</div>
              <div className="truncate text-xs text-muted-foreground">
                {item.meta}
                {typeof item.xp === 'number' ? ` · +${item.xp} XP` : ''}
              </div>
            </div>
            <span className="shrink-0 text-xs text-muted-foreground">{item.time}</span>
          </li>
        )
      })}
    </ul>
  )
}
