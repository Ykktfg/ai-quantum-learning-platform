
import {
  TrendingUp,
  Zap,
  Flame,
  BookOpenCheck,
  Trophy,
  Award,
  AlertTriangle,
  Sparkles,
  Medal,
} from 'lucide-react'
import { GlassCard, SectionHeading, ProgressBar, RingProgress, Chip } from '@/components/quantum-ui'
import { StatTile } from '@/components/analytics/stat-tile'
import { SkillMastery } from '@/components/analytics/skill-mastery'
import { ActivityChart } from '@/components/analytics/activity-chart'
import { AchievementGrid } from '@/components/analytics/achievement-grid'
import { RecommendationList } from '@/components/analytics/recommendation-list'
import { EmptyState } from '@/components/analytics/empty-state'
import { PageLoadingSkeleton } from '@/components/analytics/loading-skeleton'
import { useUserData } from '@/hooks/use-user-data'

export default function ProgressPage() {
  const { data, isLoading, error } = useUserData()

  if (isLoading) return <PageLoadingSkeleton />

  if (error || !data) {
    return (
      <div className="mx-auto max-w-7xl">
        <GlassCard className="p-8">
          <EmptyState
            icon={AlertTriangle}
            title="Couldn't load your progress"
            description={error ?? 'Please try again in a moment.'}
          />
        </GlassCard>
      </div>
    )
  }

  const { progress, skills, achievements, weeklyActivity, weakTopics, recommendations } = data
  const earnedCount = achievements.filter((a) => a.earned).length
  const xpToNext = Math.max(0, progress.nextLevelXp - progress.xp)

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      {/* page header */}
      <div>
        <div className="flex items-center gap-2 text-primary">
          <TrendingUp className="size-5" />
          <span className="text-sm font-medium tracking-wide">ANALYTICS</span>
        </div>
        <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">Your Progress</h1>
        <p className="mt-1 text-muted-foreground">Track your quantum mastery, weekly activity, and next steps.</p>
      </div>

      {/* 1. Progress overview */}
      <div className="grid gap-6 lg:grid-cols-3">
        <GlassCard glow="cyan" className="flex flex-col items-center justify-center p-6 text-center">
          <RingProgress value={progress.overallProgress} size={150} sublabel="Complete" />
          <div className="mt-4 font-semibold">
            {progress.levelTitle} · Level {progress.level}
          </div>
          <div className="mt-3 w-full">
            <div className="mb-1.5 flex justify-between text-xs text-muted-foreground">
              <span>{progress.xp.toLocaleString()} XP</span>
              <span>{progress.nextLevelXp.toLocaleString()} XP</span>
            </div>
            <ProgressBar
              value={progress.nextLevelXp ? (progress.xp / progress.nextLevelXp) * 100 : 0}
              tone="violet"
            />
            <div className="mt-1.5 text-xs text-muted-foreground">
              {xpToNext.toLocaleString()} XP to next level
            </div>
          </div>
        </GlassCard>

        <ActivityCardWrapper>
          <ActivityChart data={weeklyActivity} />
        </ActivityCardWrapper>
      </div>

      {/* stat tiles */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile
          label="Modules"
          value={`${progress.modulesCompleted}/${progress.totalModules}`}
          icon={BookOpenCheck}
        />
        <StatTile
          label="Challenges"
          value={`${progress.challengesCompleted}/${progress.totalChallenges}`}
          icon={Trophy}
        />
        <StatTile label="Day Streak" value={`${progress.streakDays}`} icon={Flame} />
        <StatTile
          label="Rank"
          value={progress.rank ? `#${progress.rank}` : 'Unranked'}
          icon={Medal}
        />
      </div>

      {/* 2. Skill progress + 5. areas to improve */}
      <div className="grid gap-6 lg:grid-cols-3">
        <GlassCard className="p-6 lg:col-span-2">
          <SkillMastery skills={skills} />

          {/* areas to improve */}
          <div className="mt-6 rounded-xl border border-chart-4/25 bg-chart-4/8 p-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-chart-4">
              <AlertTriangle className="size-4" /> Areas to Improve
            </div>
            {weakTopics.length === 0 ? (
              <p className="mt-1 text-xs text-muted-foreground">
                Great work — no weak topics right now. Keep it up!
              </p>
            ) : (
              <>
                <p className="mt-1 text-xs text-muted-foreground">
                  The AI Copilot recommends extra practice on these lower-accuracy topics.
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {weakTopics.map((t) => (
                    <Chip key={t.id} tone="amber">
                      {t.name} · {t.accuracy}%
                    </Chip>
                  ))}
                </div>
              </>
            )}
          </div>
        </GlassCard>

        {/* XP / level summary */}
        <GlassCard className="p-6">
          <SectionHeading title="Level Stats" icon={<Zap className="size-5" />} />
          <div className="space-y-4">
            <div className="flex items-center justify-between rounded-xl border border-border bg-secondary/30 p-3">
              <span className="text-sm text-muted-foreground">Total XP</span>
              <span className="font-mono font-semibold text-primary">{progress.xp.toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-border bg-secondary/30 p-3">
              <span className="text-sm text-muted-foreground">Badges unlocked</span>
              <span className="font-mono font-semibold">
                {earnedCount}/{achievements.length}
              </span>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-border bg-secondary/30 p-3">
              <span className="text-sm text-muted-foreground">Overall completion</span>
              <span className="font-mono font-semibold">{progress.overallProgress}%</span>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* 4. Achievements */}
      <GlassCard className="p-6">
        <SectionHeading
          title="Achievements"
          subtitle={`${earnedCount} of ${achievements.length} badges unlocked`}
          icon={<Award className="size-5" />}
        />
        <AchievementGrid achievements={achievements} />
      </GlassCard>

      {/* 6. Personalized recommendations */}
      <GlassCard className="p-6">
        <SectionHeading title="Personalized Recommendations" icon={<Sparkles className="size-5" />} />
        <RecommendationList recommendations={recommendations} />
      </GlassCard>
    </div>
  )
}

function ActivityCardWrapper({ children }: { children: React.ReactNode }) {
  return <GlassCard className="p-6 lg:col-span-2">{children}</GlassCard>
}
