
/**
 * QuantumVerse AI — global Dark / Light theme system.
 *
 * A tiny, dependency-free theme context that:
 *   • exposes exactly two themes: 'dark' (default) and 'light' — no "system".
 *   • applies the theme globally by toggling a `dark` / `light` class on <html>.
 *   • persists the choice in localStorage so it survives a page refresh.
 *
 * The initial class is set by an inline no-flash script in app/layout.tsx
 * BEFORE React hydrates, so there is never a flash of the wrong theme. This
 * provider then reconciles React state with what that script applied.
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

export type Theme = 'dark' | 'light'

/** localStorage key — also referenced by the inline no-flash script in layout.tsx. */
export const THEME_STORAGE_KEY = 'qv_theme'

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

/** Apply the theme to <html>: swap the class and keep native color-scheme in sync. */
function applyTheme(theme: Theme) {
  const root = document.documentElement
  root.classList.remove('dark', 'light')
  root.classList.add(theme)
  root.style.colorScheme = theme
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('dark')

  // Reconcile React state with the theme the inline script already applied.
  useEffect(() => {
    try {
      const stored = localStorage.getItem(THEME_STORAGE_KEY)
      const initial: Theme =
        stored === 'light' || stored === 'dark'
          ? stored
          : document.documentElement.classList.contains('light')
            ? 'light'
            : 'dark'
      setThemeState(initial)
      applyTheme(initial)
    } catch {
      // localStorage unavailable (e.g. private mode) — stay on the default.
    }
  }, [])

  const setTheme = useCallback((next: Theme) => {
    setThemeState(next)
    applyTheme(next)
    try {
      localStorage.setItem(THEME_STORAGE_KEY, next)
    } catch {
      // ignore storage failures — theme still applies for this session
    }
  }, [])

  const toggleTheme = useCallback(() => {
    setThemeState((prev) => {
      const next: Theme = prev === 'dark' ? 'light' : 'dark'
      applyTheme(next)
      try {
        localStorage.setItem(THEME_STORAGE_KEY, next)
      } catch {
        // ignore
      }
      return next
    })
  }, [])

  const value = useMemo<ThemeContextValue>(
    () => ({ theme, setTheme, toggleTheme }),
    [theme, setTheme, toggleTheme],
  )

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext)
  if (!ctx) {
    throw new Error('useTheme must be used within a <ThemeProvider>')
  }
  return ctx
}
