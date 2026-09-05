import { Sparkles } from 'lucide-react'
import { SectionHeading, ProgressBar } from '@/components/quantum-ui'
import { EmptyState } from '@/components/analytics/empty-state'
import type { SkillProgress } from '@/types/user'

export function SkillMastery({ skills }: { skills: SkillProgress[] }) {
  return (
    <>
      <SectionHeading title="Concept Mastery" icon={<Sparkles className="size-5" />} />
      {skills.length === 0 ? (
        <EmptyState
          icon={Sparkles}
          title="No skills tracked yet"
          description="Complete lessons to start building your quantum concept mastery."
        />
      ) : (
        <div className="space-y-5">
          {skills.map((s) => (
            <div key={s.id}>
              <div className="mb-1.5 flex items-center justify-between text-sm">
                <span className="font-medium">{s.name}</span>
                <span className="font-mono text-muted-foreground">{s.value}%</span>
              </div>
              <ProgressBar value={s.value} tone={s.tone} />
            </div>
          ))}
        </div>
      )}
    </>
  )
}
