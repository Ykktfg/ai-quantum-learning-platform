

import {
  Zap,
  Flame,
  Trophy,
  Award,
  BookOpenCheck,
  Settings,
  Atom,
  Medal,
  History,
  Mail,
  Calendar,
  AlertTriangle,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { GlassCard, SectionHeading, ProgressBar, Chip } from '@/components/quantum-ui'
import { StatTile } from '@/components/analytics/stat-tile'
import { AchievementGrid } from '@/components/analytics/achievement-grid'
import { ActivityTimeline } from '@/components/analytics/activity-timeline'
import { AccountSettings } from '@/components/analytics/account-settings'
import { EmptyState } from '@/components/analytics/empty-state'
import { PageLoadingSkeleton } from '@/components/analytics/loading-skeleton'
import { useUserData } from '@/hooks/use-user-data'

export default function ProfilePage() {
  const { data, isLoading, error } = useUserData()

  if (isLoading) return <PageLoadingSkeleton />

  if (error || !data) {
    return (
      <div className="mx-auto max-w-7xl">
        <GlassCard className="p-8">
          <EmptyState
            icon={AlertTriangle}
            title="Couldn't load your profile"
            description={error ?? 'Please try again in a moment.'}
          />
        </GlassCard>
      </div>
    )
  }

  const { user, progress, achievements, activity } = data
  const earnedCount = achievements.filter((a) => a.earned).length
  const initial = user.name.trim().charAt(0).toUpperCase() || '?'

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      {/* 1. Profile header */}
      <GlassCard glow="violet" className="relative overflow-hidden p-6 sm:p-8">
        <div className="absolute -right-8 -top-8 opacity-15">
          <Atom className="size-40 text-accent" style={{ animation: 'orbit-spin 26s linear infinite' }} />
        </div>
        <div className="relative flex flex-col items-center gap-5 sm:flex-row">
          {user.avatarUrl ? (
            <img
              src={user.avatarUrl || "/placeholder.svg"}
              alt={`${user.name}'s avatar`}
              width={80}
              height={80}
              className="size-20 rounded-2xl object-cover ring-4 ring-primary/20"
            />
          ) : (
            <span className="flex size-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-accent text-3xl font-bold text-primary-foreground ring-4 ring-primary/20">
              {initial}
            </span>
          )}

          <div className="flex-1 text-center sm:text-left">
            <h1 className="text-2xl font-bold tracking-tight">{user.name}</h1>
            <div className="mt-1 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-sm text-muted-foreground sm:justify-start">
              <span className="inline-flex items-center gap-1.5">
                <Mail className="size-3.5" /> {user.email}
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Calendar className="size-3.5" /> Joined {formatJoinDate(user.joinedAt)}
              </span>
            </div>
            <div className="mt-2 flex flex-wrap justify-center gap-2 sm:justify-start">
              <Chip tone="violet">{user.role}</Chip>
              <Chip tone="cyan">
                {progress.levelTitle} · Level {progress.level}
              </Chip>
              <Chip tone="amber">
                <Flame className="size-3.5" /> {progress.streakDays} day streak
              </Chip>
            </div>
          </div>

          <Button variant="secondary" className="rounded-xl">
            <Settings className="size-4" /> Edit Profile
          </Button>
        </div>

        {/* level progress */}
        <div className="relative mt-6">
          <div className="mb-1.5 flex justify-between text-xs text-muted-foreground">
            <span>Level progress</span>
            <span>
              {progress.xp.toLocaleString()} / {progress.nextLevelXp.toLocaleString()} XP
            </span>
          </div>
          <ProgressBar
            value={progress.nextLevelXp ? (progress.xp / progress.nextLevelXp) * 100 : 0}
            tone="cyan"
          />
        </div>
      </GlassCard>

      {/* 2. Learning statistics */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-5">
        <StatTile label="Level" value={`${progress.level}`} icon={Zap} />
        <StatTile label="XP" value={progress.xp.toLocaleString()} icon={Award} />
        <StatTile label="Day Streak" value={`${progress.streakDays}`} icon={Flame} />
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
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* 3. Achievements */}
        <GlassCard className="p-6 lg:col-span-2">
          <SectionHeading
            title="Achievements"
            subtitle={`${earnedCount} of ${achievements.length} badges unlocked`}
            icon={<Award className="size-5" />}
          />
          <AchievementGrid achievements={achievements} />
        </GlassCard>

        {/* 4. Recent learning activity */}
        <GlassCard className="p-6">
          <SectionHeading title="Recent Activity" icon={<History className="size-5" />} />
          <ActivityTimeline activity={activity} />
        </GlassCard>
      </div>

      {/* rank highlight */}
      <div className="grid gap-6 lg:grid-cols-3">
        <GlassCard className="flex items-center gap-4 p-6">
          <span className="flex size-12 items-center justify-center rounded-2xl bg-chart-4/15 text-chart-4 ring-1 ring-chart-4/30">
            <Medal className="size-6" />
          </span>
          <div>
            <div className="text-2xl font-bold tracking-tight">
              {progress.rank ? `#${progress.rank}` : 'Unranked'}
            </div>
            <div className="text-sm text-muted-foreground">Global leaderboard rank</div>
          </div>
        </GlassCard>

        {/* 5. Account settings */}
        <GlassCard className="p-6 lg:col-span-2">
          <AccountSettings user={user} />
        </GlassCard>
      </div>
    </div>
  )
}

function formatJoinDate(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}
