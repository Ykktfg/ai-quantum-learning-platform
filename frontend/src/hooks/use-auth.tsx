
/**
 * QuantumVerse AI — TEMPORARY frontend-only demo authentication.
 *
 * ⚠️  There is NO real backend, no database, no JWT, and no password hashing
 *     here. This context only simulates an auth session in the browser
 *     (persisted to localStorage) so the UI can gate access to the app and
 *     flow a "current user" into the existing Profile/Progress data layer.
 *
 * ── HOW TO GO LIVE ─────────────────────────────────────────────────────────
 * The public API of this context (`login`, `signup`, `logout`, `user`,
 * `isAuthenticated`) is intentionally shaped like a real auth client. The
 * backend team can replace the bodies of `login` / `signup` / `logout` /
 * the bootstrap effect with real API calls (e.g. POST /auth/login returning a
 * session cookie or token) WITHOUT changing any page or component:
 *
 *   const login: AuthContextValue['login'] = async ({ identifier, password }) => {
 *     const res = await fetch('/api/auth/login', {
 *       method: 'POST',
 *       headers: { 'Content-Type': 'application/json' },
 *       body: JSON.stringify({ identifier, password }),
 *       credentials: 'include',
 *     })
 *     if (!res.ok) throw new Error('Invalid credentials')
 *     setUser((await res.json()) as AuthUser)
 *   }
 * ───────────────────────────────────────────────────────────────────────────
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

/** The authenticated user's identity (matches the identity fields the API will return). */
export interface AuthUser {
  id: string
  name: string
  username: string
  email: string
}

export interface LoginInput {
  /** Email OR username. */
  identifier: string
  password: string
  remember?: boolean
}

export interface SignupInput {
  name: string
  username: string
  email: string
  password: string
}

export interface AuthContextValue {
  user: AuthUser | null
  isAuthenticated: boolean
  /** True until the persisted session has been read on first mount (avoids UI flash). */
  isInitializing: boolean
  login: (input: LoginInput) => Promise<AuthUser>
  signup: (input: SignupInput) => Promise<AuthUser>
  logout: () => void
}

const SESSION_KEY = 'qv_demo_session'
const REGISTRY_KEY = 'qv_demo_users'

const AuthContext = createContext<AuthContextValue | null>(null)

/** Small helper: turn an email/identifier into a friendly display name for demo logins. */
function deriveNameFromIdentifier(identifier: string): string {
  const base = identifier.includes('@') ? identifier.split('@')[0] : identifier
  return base
    .replace(/[._-]+/g, ' ')
    .split(' ')
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ') || 'Quantum Learner'
}

/** Demo-only local registry so a signed-up user can "log in" again with a nice name. */
function readRegistry(): Array<AuthUser & { password: string }> {
  try {
    const raw = localStorage.getItem(REGISTRY_KEY)
    return raw ? (JSON.parse(raw) as Array<AuthUser & { password: string }>) : []
  } catch {
    return []
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isInitializing, setIsInitializing] = useState(true)

  // Bootstrap: restore any persisted demo session on first mount.
  useEffect(() => {
    try {
      const raw = localStorage.getItem(SESSION_KEY)
      if (raw) setUser(JSON.parse(raw) as AuthUser)
    } catch {
      // ignore corrupt/unavailable storage
    } finally {
      setIsInitializing(false)
    }
  }, [])

  const persistSession = useCallback((next: AuthUser) => {
    setUser(next)
    try {
      localStorage.setItem(SESSION_KEY, JSON.stringify(next))
    } catch {
      // storage may be unavailable (private mode) — session stays in memory
    }
  }, [])

  const login = useCallback<AuthContextValue['login']>(
    async ({ identifier, password }) => {
      // ── DEMO ONLY: accept any non-empty credentials. Replace with a real API call. ──
      await new Promise((r) => setTimeout(r, 500)) // simulate network latency
      if (!identifier.trim() || !password.trim()) {
        throw new Error('Please enter your credentials.')
      }
      const match = readRegistry().find(
        (u) => u.email === identifier.trim() || u.username === identifier.trim(),
      )
      const authUser: AuthUser = match
        ? { id: match.id, name: match.name, username: match.username, email: match.email }
        : {
            id: `usr_${Math.random().toString(36).slice(2, 10)}`,
            name: deriveNameFromIdentifier(identifier.trim()),
            username: identifier.includes('@') ? identifier.split('@')[0] : identifier.trim(),
            email: identifier.includes('@') ? identifier.trim() : `${identifier.trim()}@quantumverse.ai`,
          }
      persistSession(authUser)
      return authUser
    },
    [persistSession],
  )

  const signup = useCallback<AuthContextValue['signup']>(
    async ({ name, username, email, password }) => {
      // ── DEMO ONLY: no server registration. Replace with a real API call. ──
      await new Promise((r) => setTimeout(r, 600)) // simulate network latency
      const authUser: AuthUser = {
        id: `usr_${Math.random().toString(36).slice(2, 10)}`,
        name: name.trim(),
        username: username.trim(),
        email: email.trim(),
      }
      // Remember this demo user locally so a later login re-uses their name.
      try {
        const registry = readRegistry().filter((u) => u.email !== authUser.email)
        registry.push({ ...authUser, password })
        localStorage.setItem(REGISTRY_KEY, JSON.stringify(registry))
      } catch {
        // ignore storage failures
      }
      persistSession(authUser)
      return authUser
    },
    [persistSession],
  )

  const logout = useCallback(() => {
    setUser(null)
    try {
      localStorage.removeItem(SESSION_KEY)
    } catch {
      // ignore
    }
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({ user, isAuthenticated: user !== null, isInitializing, login, signup, logout }),
    [user, isInitializing, login, signup, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within an <AuthProvider>')
  }
  return ctx
}
