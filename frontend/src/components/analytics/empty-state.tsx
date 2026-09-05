import type { LucideIcon } from 'lucide-react'

export interface EmptyStateProps {
  icon: LucideIcon
  title: string
  description: string
}

/** Compact zero-state used inside sections that have no data yet. */
export function EmptyState({ icon: Icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-secondary/20 px-6 py-10 text-center">
      <span className="flex size-12 items-center justify-center rounded-2xl bg-secondary/60 text-muted-foreground ring-1 ring-border">
        <Icon className="size-6" />
      </span>
      <div className="mt-3 text-sm font-semibold">{title}</div>
      <p className="mt-1 max-w-xs text-xs text-muted-foreground">{description}</p>
    </div>
  )
}
