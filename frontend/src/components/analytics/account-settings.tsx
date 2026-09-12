
import { useState } from 'react'
import { UserCog, Bell, Palette, Check, Moon, Sun } from 'lucide-react'
import { SectionHeading } from '@/components/quantum-ui'
import { Button } from '@/components/ui/button'
import type { User } from '@/types/user'
import { useTheme, type Theme } from '@/hooks/use-theme'
import { cn } from '@/lib/utils'

type Tab = 'profile' | 'notifications' | 'appearance'

const TABS: { id: Tab; label: string; icon: typeof UserCog }[] = [
  { id: 'profile', label: 'Profile', icon: UserCog },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'appearance', label: 'Appearance', icon: Palette },
]

/**
 * Frontend-only settings UI. No values are persisted — state is local so the
 * backend team can wire real mutations later without restructuring the UI.
 */
export function AccountSettings({ user }: { user: User }) {
  const [tab, setTab] = useState<Tab>('profile')

  return (
    <>
      <SectionHeading title="Account Settings" icon={<UserCog className="size-5" />} />

      <div className="flex flex-wrap gap-2">
        {TABS.map((t) => {
          const Icon = t.icon
          const active = tab === t.id
          return (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={cn(
                'inline-flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition-colors',
                active
                  ? 'bg-primary/12 text-primary ring-1 ring-primary/25'
                  : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground',
              )}
            >
              <Icon className="size-4" />
              {t.label}
            </button>
          )
        })}
      </div>

      <div className="mt-5">
        {tab === 'profile' ? <ProfileSettings user={user} /> : null}
        {tab === 'notifications' ? <NotificationSettings /> : null}
        {tab === 'appearance' ? <AppearanceSettings /> : null}
      </div>
    </>
  )
}

function Field({ label, defaultValue, type = 'text' }: { label: string; defaultValue: string; type?: string }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium text-muted-foreground">{label}</span>
      <input
        type={type}
        defaultValue={defaultValue}
        className="w-full rounded-xl border border-border bg-secondary/30 px-3 py-2 text-sm outline-none ring-primary/30 transition focus:ring-2"
      />
    </label>
  )
}

function ProfileSettings({ user }: { user: User }) {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Full name" defaultValue={user.name} />
        <Field label="Email" defaultValue={user.email} type="email" />
        <Field label="Role" defaultValue={user.role} />
        <Field label="Member since" defaultValue={formatJoinDate(user.joinedAt)} />
      </div>
      <Button className="rounded-xl">
        <Check className="size-4" /> Save changes
      </Button>
    </div>
  )
}

const NOTIFICATION_OPTIONS = [
  { id: 'streak', label: 'Daily streak reminders', desc: 'Nudge me so I keep my learning streak alive.', on: true },
  { id: 'achievements', label: 'Achievement unlocks', desc: 'Tell me when I earn a new badge.', on: true },
  { id: 'recommendations', label: 'AI recommendations', desc: 'Weekly personalized study suggestions.', on: false },
  { id: 'leaderboard', label: 'Leaderboard changes', desc: 'Alert me when my rank changes.', on: false },
]

function NotificationSettings() {
  return (
    <div className="space-y-3">
      {NOTIFICATION_OPTIONS.map((o) => (
        <Toggle key={o.id} label={o.label} desc={o.desc} defaultOn={o.on} />
      ))}
    </div>
  )
}

const THEME_OPTIONS: { id: Theme; label: string; desc: string; icon: typeof Moon }[] = [
  { id: 'dark', label: 'Dark', desc: 'Futuristic quantum interface', icon: Moon },
  { id: 'light', label: 'Light', desc: 'Clean, professional daylight', icon: Sun },
]

function AppearanceSettings() {
  const { theme, setTheme } = useTheme()
  return (
    <div className="space-y-5">
      <div>
        <span className="mb-2 block text-xs font-medium text-muted-foreground">Theme</span>
        <div className="grid gap-3 sm:grid-cols-2">
          {THEME_OPTIONS.map((opt) => {
            const Icon = opt.icon
            const active = theme === opt.id
            return (
              <button
                key={opt.id}
                onClick={() => setTheme(opt.id)}
                aria-pressed={active}
                className={cn(
                  'flex items-center gap-3 rounded-xl border px-4 py-3 text-left transition-colors',
                  active
                    ? 'border-primary/40 bg-primary/10 text-foreground ring-1 ring-primary/25'
                    : 'border-border bg-secondary/30 text-muted-foreground hover:text-foreground',
                )}
              >
                <span
                  className={cn(
                    'flex size-9 shrink-0 items-center justify-center rounded-lg',
                    active ? 'bg-primary/15 text-primary' : 'bg-secondary text-muted-foreground',
                  )}
                >
                  <Icon className="size-4.5" />
                </span>
                <span className="min-w-0">
                  <span className="flex items-center gap-1.5 text-sm font-medium">
                    {opt.label}
                    {active ? <Check className="size-3.5 text-primary" /> : null}
                  </span>
                  <span className="block truncate text-xs text-muted-foreground">{opt.desc}</span>
                </span>
              </button>
            )
          })}
        </div>
      </div>
      <Toggle label="Reduced motion" desc="Minimize background quantum animations." defaultOn={false} />
      <Toggle label="Compact layout" desc="Tighter spacing across the dashboard." defaultOn={false} />
    </div>
  )
}

function Toggle({ label, desc, defaultOn }: { label: string; desc: string; defaultOn: boolean }) {
  const [on, setOn] = useState(defaultOn)
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl border border-border bg-secondary/30 p-3">
      <div className="min-w-0">
        <div className="text-sm font-medium">{label}</div>
        <div className="text-xs text-muted-foreground">{desc}</div>
      </div>
      <button
        role="switch"
        aria-checked={on}
        aria-label={label}
        onClick={() => setOn((v) => !v)}
        className={cn(
          'relative h-6 w-11 shrink-0 rounded-full transition-colors',
          on ? 'bg-primary' : 'bg-secondary',
        )}
      >
        <span
          className={cn(
            'absolute top-0.5 size-5 rounded-full bg-background transition-transform',
            on ? 'translate-x-5' : 'translate-x-0.5',
          )}
        />
      </button>
    </div>
  )
}

function formatJoinDate(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}
