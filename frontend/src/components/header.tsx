
import { Menu, Search, Bell, Flame, Zap, LogOut, Moon, Sun } from 'lucide-react'
import { Chip } from '@/components/quantum-ui'
import { student } from '@/lib/data'
import { useAuth } from '@/hooks/use-auth'
import { useTheme } from '@/hooks/use-theme'

export function Header({ onMenu }: { onMenu: () => void }) {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const displayName = user?.name ?? student.name

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-border bg-background/70 px-4 backdrop-blur-xl sm:px-6">
      <button
        onClick={onMenu}
        className="flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground lg:hidden"
        aria-label="Open navigation"
      >
        <Menu className="size-5" />
      </button>

      {/* search */}
      <div className="relative hidden max-w-md flex-1 sm:block">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="search"
          placeholder="Search lessons, gates, algorithms…"
          className="h-10 w-full rounded-xl border border-border bg-secondary/40 pl-9 pr-4 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-primary/40 focus:bg-secondary/70"
        />
      </div>

      <div className="ml-auto flex items-center gap-2 sm:gap-3">
        <Chip tone="amber" className="hidden sm:inline-flex">
          <Flame className="size-3.5" />
          {student.streak} day streak
        </Chip>
        <Chip tone="cyan" className="hidden sm:inline-flex">
          <Zap className="size-3.5" />
          {student.xp.toLocaleString()} XP
        </Chip>

        <button
          onClick={toggleTheme}
          className="flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
        >
          {theme === 'dark' ? <Sun className="size-5" /> : <Moon className="size-5" />}
        </button>

        <button
          className="relative flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label="Notifications"
        >
          <Bell className="size-5" />
          <span className="absolute right-2 top-2 size-2 rounded-full bg-accent ring-2 ring-background" />
        </button>

        <div className="flex items-center gap-2.5 rounded-xl border border-border bg-secondary/40 py-1 pl-1 pr-3">
          <span className="flex size-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent text-sm font-bold text-primary-foreground">
            {displayName.charAt(0).toUpperCase()}
          </span>
          <div className="hidden leading-tight sm:block">
            <div className="text-sm font-medium">{displayName}</div>
            <div className="text-[11px] text-muted-foreground">{student.level}</div>
          </div>
        </div>

        <button
          onClick={logout}
          className="flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label="Log out"
          title="Log out"
        >
          <LogOut className="size-5" />
        </button>
      </div>
    </header>
  )
}
