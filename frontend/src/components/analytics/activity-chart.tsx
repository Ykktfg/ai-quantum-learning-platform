import { TrendingUp } from 'lucide-react'
import { SectionHeading } from '@/components/quantum-ui'
import { EmptyState } from '@/components/analytics/empty-state'
import type { DailyActivity } from '@/types/user'

export function ActivityChart({ data }: { data: DailyActivity[] }) {
  const totalMinutes = data.reduce((s, d) => s + d.minutes, 0)
  const maxMinutes = Math.max(1, ...data.map((d) => d.minutes))

  return (
    <>
      <SectionHeading
        title="Weekly Activity"
        subtitle={data.length ? `${totalMinutes} minutes this week` : 'Your study time will appear here'}
        icon={<TrendingUp className="size-5" />}
      />
      {data.length === 0 ? (
        <EmptyState
          icon={TrendingUp}
          title="No activity this week"
          description="Study a lesson or challenge and your weekly minutes will show up here."
        />
      ) : (
        <div className="flex h-48 items-end justify-between gap-3">
          {data.map((d) => (
            <div key={d.day} className="flex h-full flex-1 flex-col items-center justify-end gap-2">
              <div
                className="w-full max-w-10 rounded-t-lg bg-gradient-to-t from-primary/40 to-primary transition-all duration-700 hover:from-accent/50 hover:to-accent"
                style={{ height: `${(d.minutes / maxMinutes) * 100}%` }}
                title={`${d.minutes} min`}
              />
              <span className="text-xs text-muted-foreground">{d.day}</span>
            </div>
          ))}
        </div>
      )}
    </>
  )
}
