import { Link } from 'react-router-dom'
import { Sparkles, ArrowRight } from 'lucide-react'
import { EmptyState } from '@/components/analytics/empty-state'
import { Chip } from '@/components/quantum-ui'
import { resolveIcon } from '@/components/analytics/icon-map'
import type { Recommendation } from '@/types/user'

export function RecommendationList({ recommendations }: { recommendations: Recommendation[] }) {
  if (recommendations.length === 0) {
    return (
      <EmptyState
        icon={Sparkles}
        title="No recommendations yet"
        description="As you learn, the AI Copilot will suggest personalized next steps here."
      />
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {recommendations.map((r) => {
        const Icon = resolveIcon(r.icon)
        const body = (
          <div className="group flex h-full flex-col rounded-xl border border-border bg-secondary/30 p-4 transition-colors hover:border-primary/30 hover:bg-primary/5">
            <div className="flex items-center justify-between">
              <span className="flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
                <Icon className="size-5" />
              </span>
              <Chip tone="violet">{r.reason}</Chip>
            </div>
            <div className="mt-3 text-sm font-semibold">{r.title}</div>
            <p className="mt-1 flex-1 text-xs text-muted-foreground">{r.description}</p>
            {r.href ? (
              <span className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-primary">
                Start now
                <ArrowRight className="size-3.5 transition-transform group-hover:translate-x-0.5" />
              </span>
            ) : null}
          </div>
        )
        return r.href ? (
          <Link key={r.id} to={r.href} className="block h-full">
            {body}
          </Link>
        ) : (
          <div key={r.id}>{body}</div>
        )
      })}
    </div>
  )
}
