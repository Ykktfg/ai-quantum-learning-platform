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
 * Profile and Progress both use this hook.
 *
 * The current dashboard/profile UI uses the existing demo data while
 * authentication is handled by the real backend.
 */
async function fetchCurrentUserData(): Promise<CurrentUserData> {
  // Small delay so the loading state/skeleton remains visible.
  await new Promise((resolve) => setTimeout(resolve, 300))

  return mockCurrentUserData
}

export function useUserData(): UseUserDataResult {
  const { user: authUser } = useAuth()

  const [data, setData] =
    useState<CurrentUserData | null>(null)

  const [isLoading, setIsLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  useEffect(() => {
    let active = true

    setIsLoading(true)
    setError(null)

    fetchCurrentUserData()
      .then((result) => {
        if (!active) return

        /*
         * Use the real logged-in user's identity while keeping
         * the existing demo progress/achievement/activity data.
         */
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
        if (!active) return

        setError(
          err instanceof Error
            ? err.message
            : 'Something went wrong',
        )
      })
      .finally(() => {
        if (active) {
          setIsLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [authUser])

  return {
    data,
    isLoading,
    error,
  }
}