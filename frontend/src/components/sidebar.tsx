
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  GraduationCap,
  CircuitBoard,
  Bot,
  Trophy,
  TrendingUp,
  User,
  Atom,
  PanelLeftClose,
  PanelLeft,
  Sparkles,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const NAV = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/learn', label: 'Learn', icon: GraduationCap },
  { href: '/lab', label: 'Quantum Circuit Lab', icon: CircuitBoard },
  { href: '/copilot', label: 'AI Quantum Copilot', icon: Bot },
  { href: '/challenges', label: 'Challenges', icon: Trophy },
  { href: '/progress', label: 'Progress', icon: TrendingUp },
  { href: '/profile', label: 'Profile', icon: User },
  { href: '/lab', label: 'Quantum Circuit Lab', icon: CircuitBoard },
  { href: '/algorithms', label: 'Algorithms', icon: Atom },
]

export function Sidebar({
  collapsed,
  onToggle,
  mobileOpen,
  onMobileClose,
}: {
  collapsed: boolean
  onToggle: () => void
  mobileOpen: boolean
  onMobileClose: () => void
}) {
  const { pathname } = useLocation()

  return (
    <>
      {/* mobile backdrop */}
      {mobileOpen ? (
        <div
          className="fixed inset-0 z-40 bg-background/70 backdrop-blur-sm lg:hidden"
          onClick={onMobileClose}
          aria-hidden
        />
      ) : null}

      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex flex-col border-r border-sidebar-border bg-sidebar transition-[width,transform] duration-300 ease-out',
          collapsed ? 'w-[76px]' : 'w-[264px]',
          mobileOpen ? 'translate-x-0' : '-translate-x-full',
          'lg:translate-x-0',
        )}
      >
        {/* logo */}
        <div className={cn('flex h-16 items-center gap-3 px-4', collapsed && 'justify-center px-0')}>
          <span className="relative flex size-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary/25 to-accent/25 ring-1 ring-primary/30">
            <Atom className="size-5 text-primary" style={{ animation: 'orbit-spin 12s linear infinite' }} />
          </span>
          {!collapsed ? (
            <div className="leading-tight">
              <div className="font-semibold tracking-tight">
                Quantum<span className="text-primary">Verse</span>
              </div>
              <div className="text-[11px] font-medium tracking-wide text-muted-foreground">AI PLATFORM</div>
            </div>
          ) : null}
        </div>

        {/* nav */}
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
          {NAV.map((item) => {
            const active = pathname === item.href
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                to={item.href}
                onClick={onMobileClose}
                title={collapsed ? item.label : undefined}
                className={cn(
                  'group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors',
                  collapsed && 'justify-center px-0',
                  active
                    ? 'bg-primary/12 text-primary ring-1 ring-primary/25'
                    : 'text-sidebar-foreground/75 hover:bg-sidebar-accent hover:text-sidebar-foreground',
                )}
              >
                {active ? (
                  <span className="absolute left-0 top-1/2 h-6 -translate-y-1/2 rounded-r-full bg-primary" style={{ width: 3 }} />
                ) : null}
                <Icon className={cn('size-5 shrink-0', active && 'text-glow')} />
                {!collapsed ? <span className="truncate">{item.label}</span> : null}
              </Link>
            )
          })}
        </nav>

        {/* upgrade / tagline card */}
        {!collapsed ? (
          <div className="mx-3 mb-3 rounded-xl bg-gradient-to-br from-primary/12 to-accent/12 p-3 ring-1 ring-primary/20">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <Sparkles className="size-4 text-accent" />
              Pro Simulator
            </div>
            <p className="mt-1 text-xs text-muted-foreground">Unlock 20-qubit circuits and noise models.</p>
          </div>
        ) : null}

        {/* collapse toggle */}
        <button
          onClick={onToggle}
          className={cn(
            'm-3 hidden items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-muted-foreground transition-colors hover:bg-sidebar-accent hover:text-foreground lg:flex',
            collapsed && 'justify-center px-0',
          )}
        >
          {collapsed ? <PanelLeft className="size-5" /> : <PanelLeftClose className="size-5" />}
          {!collapsed ? <span>Collapse</span> : null}
        </button>
      </aside>
    </>
  )
}
