
import { useEffect, useState } from 'react'
import type { CurrentUserData } from '@/types/user'
import { mockCurrentUserData } from '@/data/mockUserData'
import { useAuth } from '@/hooks/use-auth'

export interface UseUserDataResult {
  data: CurrentUserData | null
  isLoading: boolean
  error: string | null
}

/**
 * Single source of truth for the current user's data across the frontend.
 *
 * ── HOW TO GO LIVE ─────────────────────────────────────────────────────────
 * Right now this resolves the temporary mock payload after a short delay so the
 * UI can exercise its loading state. To connect the real backend, replace the
 * body of `fetchCurrentUserData` with a real request, e.g.:
 *
 *   async function fetchCurrentUserData(): Promise<CurrentUserData> {
 *     const res = await fetch('/api/me/dashboard', { credentials: 'include' })
 *     if (!res.ok) throw new Error('Failed to load user data')
 *     return (await res.json()) as CurrentUserData
 *   }
 *
 * As long as the endpoint returns the `CurrentUserData` shape, no page or
 * component needs to change.
 * ───────────────────────────────────────────────────────────────────────────
 */
async function fetchCurrentUserData(): Promise<CurrentUserData> {
  // Simulated network latency for realistic loading UX. Remove when wiring real API.
  await new Promise((resolve) => setTimeout(resolve, 500))
  return mockCurrentUserData
}

export function useUserData(): UseUserDataResult {
  const { user: authUser } = useAuth()
  const [data, setData] = useState<CurrentUserData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    setIsLoading(true)
    setError(null)

    fetchCurrentUserData()
      .then((result) => {
        if (!active) return
        // Overlay the authenticated user's identity onto the current-user payload
        // so the logged-in account flows into the Profile/Progress UI. The sample
        // progress/skills/achievements stay as demo data until the backend returns
        // them per-user. With a real API this merge goes away — the endpoint would
        // already return the correct user.
        const merged: CurrentUserData = authUser
          ? {
              ...result,
              user: {
                ...result.user,
                id: authUser.id,
                name: authUser.name,
                email: authUser.email,
              },
            }
          : result
        setData(merged)
      })
      .catch((err: unknown) => {
        if (active) setError(err instanceof Error ? err.message : 'Something went wrong')
      })
      .finally(() => {
        if (active) setIsLoading(false)
      })

    return () => {
      active = false
    }
  }, [authUser])

  return { data, isLoading, error }
}
