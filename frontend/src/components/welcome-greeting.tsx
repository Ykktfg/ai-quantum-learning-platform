
import { useAuth } from '@/hooks/use-auth'

/**
 * Renders the dashboard hero greeting using the *authenticated* user's name.
 * Never falls back to a fixed demo identity — if no session is resolved yet it
 * uses a neutral greeting so we don't flash someone else's name.
 */
export function WelcomeGreeting({ overallProgress }: { overallProgress: number }) {
  const { user } = useAuth()
  const firstName = user?.name.trim().split(' ').filter(Boolean)[0]

  return (
    <>
      <h1 className="mt-4 text-balance text-2xl font-bold tracking-tight sm:text-3xl">
        {firstName ? `Welcome back, ${firstName}` : 'Welcome back'}
      </h1>
      <p className="mt-2 text-pretty text-muted-foreground">
        You&apos;re {overallProgress}% through your quantum journey. Keep the momentum going and tackle
        Entanglement next.
      </p>
    </>
  )
}
