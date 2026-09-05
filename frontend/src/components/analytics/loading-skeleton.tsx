import { GlassCard } from '@/components/quantum-ui'
import { cn } from '@/lib/utils'

function Shimmer({ className }: { className?: string }) {
  return <div className={cn('animate-pulse rounded-lg bg-secondary/60', className)} />
}

/** Full-page loading placeholder shared by Progress and Profile pages. */
export function PageLoadingSkeleton() {
  return (
    <div className="mx-auto max-w-7xl space-y-6" aria-busy="true" aria-live="polite">
      <span className="sr-only">Loading your data…</span>
      <div className="space-y-2">
        <Shimmer className="h-4 w-24" />
        <Shimmer className="h-8 w-64" />
        <Shimmer className="h-4 w-80" />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <GlassCard className="flex flex-col items-center gap-4 p-6">
          <Shimmer className="size-36 rounded-full" />
          <Shimmer className="h-4 w-40" />
          <Shimmer className="h-2 w-full" />
        </GlassCard>
        <GlassCard className="p-6 lg:col-span-2">
          <Shimmer className="mb-5 h-6 w-40" />
          <Shimmer className="h-40 w-full" />
        </GlassCard>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <GlassCard key={i} className="space-y-3 p-4">
            <Shimmer className="size-5" />
            <Shimmer className="h-7 w-16" />
            <Shimmer className="h-4 w-20" />
          </GlassCard>
        ))}
      </div>

      <GlassCard className="space-y-4 p-6">
        <Shimmer className="h-6 w-48" />
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Shimmer key={i} className="h-32 w-full" />
          ))}
        </div>
      </GlassCard>
    </div>
  )
}
