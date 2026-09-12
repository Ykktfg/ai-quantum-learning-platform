import type { LucideIcon } from 'lucide-react'
import { GlassCard } from '@/components/quantum-ui'

export interface StatTileProps {
  label: string
  value: string
  icon: LucideIcon
  hint?: string
}

export function StatTile({ label, value, icon: Icon, hint }: StatTileProps) {
  return (
    <GlassCard className="p-4">
      <Icon className="size-5 text-primary" />
      <div className="mt-3 text-2xl font-bold tracking-tight">{value}</div>
      <div className="text-sm text-muted-foreground">{label}</div>
      {hint ? <div className="mt-1 text-xs text-muted-foreground/70">{hint}</div> : null}
    </GlassCard>
  )
}
