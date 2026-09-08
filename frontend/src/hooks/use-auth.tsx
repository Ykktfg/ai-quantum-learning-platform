import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

export interface AuthUser {
  id: string
  name: string
  username: string
  email: string
  role?: string
}

export interface LoginInput {
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
  isInitializing: boolean
  login: (input: LoginInput) => Promise<AuthUser>
  signup: (input: SignupInput) => Promise<AuthUser>
  logout: () => void
}

/*
 * IMPORTANT:
 * 8000 = Quantum Engine
 * 8001 = Backend / Authentication
 */
const API_URL = 'http://127.0.0.1:8001'

const TOKEN_KEY = 'qv_access_token'
const USER_KEY = 'qv_auth_user'

const AuthContext = createContext<AuthContextValue | null>(null)

function saveAuth(
  token: string,
  user: AuthUser,
  remember = true,
) {
  const storage = remember ? localStorage : sessionStorage

  storage.setItem(TOKEN_KEY, token)
  storage.setItem(USER_KEY, JSON.stringify(user))
}

function loadAuth(): {
  token: string
  user: AuthUser
} | null {
  try {
    const sources = [localStorage, sessionStorage]

    for (const storage of sources) {
      const token = storage.getItem(TOKEN_KEY)
      const rawUser = storage.getItem(USER_KEY)

      if (token && rawUser) {
        return {
          token,
          user: JSON.parse(rawUser) as AuthUser,
        }
      }
    }
  } catch {
    // Ignore invalid storage data.
  }

  return null
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)

  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(USER_KEY)
}

export function AuthProvider({
  children,
}: {
  children: ReactNode
}) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isInitializing, setIsInitializing] =
    useState(true)

  useEffect(() => {
    const saved = loadAuth()

    if (saved) {
      setUser(saved.user)
    }

    setIsInitializing(false)
  }, [])

  const login = useCallback<AuthContextValue['login']>(
    async ({
      identifier,
      password,
      remember = true,
    }) => {
      if (!identifier.trim() || !password.trim()) {
        throw new Error(
          'Please enter your credentials.',
        )
      }

      const body = new URLSearchParams()

      body.set('username', identifier.trim())
      body.set('password', password)

      let response: Response

      try {
        response = await fetch(
          `${API_URL}/api/auth/login`,
          {
            method: 'POST',
            headers: {
              'Content-Type':
                'application/x-www-form-urlencoded',
            },
            body: body.toString(),
          },
        )
      } catch {
        throw new Error(
          'Cannot connect to the backend. Make sure the backend is running on port 8001.',
        )
      }

      if (!response.ok) {
        let message = 'Invalid email or password.'

        try {
          const error = await response.json()

          if (typeof error?.detail === 'string') {
            message = error.detail
          } else if (error?.detail) {
            message = JSON.stringify(error.detail)
          }
        } catch {
          try {
            const text = await response.text()

            if (text) {
              message = text
            }
          } catch {
            // Keep default error message.
          }
        }

        throw new Error(
          `${message} (HTTP ${response.status})`,
        )
      }

      let data: any

      try {
        data = await response.json()
      } catch {
        throw new Error(
          'Backend returned an invalid login response.',
        )
      }

      if (!data.access_token || !data.user) {
        throw new Error(
          'Backend returned an invalid login response.',
        )
      }

      const authUser: AuthUser = {
        id: String(data.user.id),
        name: data.user.name,
        username:
          data.user.username ??
          data.user.email ??
          identifier.trim(),
        email:
          data.user.email ??
          identifier.trim(),
        role: data.user.role,
      }

      saveAuth(
        data.access_token,
        authUser,
        remember,
      )

      setUser(authUser)

      return authUser
    },
    [],
  )

  const signup = useCallback<AuthContextValue['signup']>(
    async () => {
      throw new Error(
        'Signup is not connected to the backend yet. Please use an existing backend account.',
      )
    },
    [],
  )

  const logout = useCallback(() => {
    setUser(null)
    clearAuth()
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isInitializing,
      login,
      signup,
      logout,
    }),
    [
      user,
      isInitializing,
      login,
      signup,
      logout,
    ],
  )

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)

  if (!ctx) {
    throw new Error(
      'useAuth must be used within an <AuthProvider>',
    )
  }

  return ctx
}