
import { useEffect, useState, type ReactNode } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Atom } from 'lucide-react'
import { Sidebar } from '@/components/sidebar'
import { Header } from '@/components/header'
import { QuantumBackground } from '@/components/quantum-background'
import { useAuth } from '@/hooks/use-auth'
import { cn } from '@/lib/utils'

/** Routes that render without the app chrome and are reachable while logged out. */
const AUTH_ROUTES = ['/login', '/signup']

function FullScreenLoader() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <QuantumBackground />
      <div className="relative z-10 flex flex-col items-center gap-3 text-muted-foreground">
        <Atom className="size-8 text-primary" style={{ animation: 'orbit-spin 3s linear infinite' }} />
        <span className="text-sm">Loading QuantumVerse…</span>
      </div>
    </div>
  )
}

export function AppShell({ children }: { children: ReactNode }) {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { isAuthenticated, isInitializing } = useAuth()
  const isAuthRoute = AUTH_ROUTES.includes(pathname)

  // Frontend-only route guard: send guests to /login and logged-in users away
  // from the auth screens. A real backend would additionally verify the session.
  useEffect(() => {
    if (isInitializing) return
    if (!isAuthenticated && !isAuthRoute) {
      navigate('/login', { replace: true })
    } else if (isAuthenticated && isAuthRoute) {
      navigate('/', { replace: true })
    }
  }, [isAuthenticated, isInitializing, isAuthRoute, navigate])

  // Wait until the persisted session is resolved to avoid a flash of the wrong UI.
  if (isInitializing) {
    return <FullScreenLoader />
  }

  // Auth pages render standalone (their own full-screen layout, no sidebar/header).
  if (isAuthRoute) {
    return <>{children}</>
  }

  // Guest hitting a protected route: show loader while the redirect above runs.
  if (!isAuthenticated) {
    return <FullScreenLoader />
  }

  return (
    <div className="min-h-screen">
      <QuantumBackground />
      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((c) => !c)}
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
      />
      <div className={cn('flex min-h-screen flex-col transition-[padding] duration-300', collapsed ? 'lg:pl-[76px]' : 'lg:pl-[264px]')}>
        <Header onMenu={() => setMobileOpen(true)} />
        <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">{children}</main>
      </div>
    </div>
  )
}
