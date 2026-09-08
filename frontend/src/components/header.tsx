import { useMemo, useState } from 'react'
import {
  Menu,
  Search,
  Flame,
  Zap,
  LogOut,
  Moon,
  Sun,
  BookOpen,
  Cpu,
  Bot,
  Trophy,
  BarChart3,
  User,
  Atom,
  X,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { Chip } from '@/components/quantum-ui'
import { student } from '@/lib/data'
import { useAuth } from '@/hooks/use-auth'
import { useTheme } from '@/hooks/use-theme'

type SearchItem = {
  title: string
  description: string
  icon: typeof BookOpen
  href: string
  keywords: string[]
}

const searchItems: SearchItem[] = [
  {
    title: 'Learn',
    description: 'Quantum computing lessons and concepts',
    icon: BookOpen,
    href: '/learn',
    keywords: [
      'learn',
      'lesson',
      'lessons',
      'quantum',
      'learning',
      'course',
      'courses',
    ],
  },
  {
    title: 'Circuit Lab',
    description: 'Build and simulate quantum circuits',
    icon: Cpu,
    href: '/lab',
    keywords: [
      'simulate',
      'simulation',
      'circuit',
      'circuits',
      'lab',
      'gate',
      'gates',
      'qubit',
      'qubits',
    ],
  },
  {
    title: 'AI Quantum Copilot',
    description: 'Ask the AI about quantum computing',
    icon: Bot,
    href: '/copilot',
    keywords: [
      'ai',
      'copilot',
      'assistant',
      'tutor',
      'explain',
      'explanation',
    ],
  },
  {
    title: 'Challenges',
    description: 'Test your quantum computing skills',
    icon: Trophy,
    href: '/challenges',
    keywords: [
      'challenge',
      'challenges',
      'quiz',
      'test',
      'practice',
    ],
  },
  {
    title: 'Progress',
    description: 'Track your learning progress',
    icon: BarChart3,
    href: '/progress',
    keywords: [
      'progress',
      'stats',
      'statistics',
      'performance',
      'xp',
      'streak',
    ],
  },
  {
    title: 'Profile',
    description: 'View your student profile',
    icon: User,
    href: '/profile',
    keywords: ['profile', 'student', 'account', 'user'],
  },
  {
    title: 'Algorithms',
    description: 'Explore quantum algorithms',
    icon: Atom,
    href: '/algorithms',
    keywords: [
      'algorithm',
      'algorithms',
      'grover',
      'shor',
      'qft',
      'search',
    ],
  },
]

export function Header({ onMenu }: { onMenu: () => void }) {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()

  const displayName = user?.name ?? student.name

  const [searchQuery, setSearchQuery] = useState('')
  const [searchFocused, setSearchFocused] = useState(false)

  const filteredResults = useMemo(() => {
    const query = searchQuery.trim().toLowerCase()

    if (!query) {
      return []
    }

    return searchItems
      .filter((item) => {
        const searchableText = [
          item.title,
          item.description,
          ...item.keywords,
        ]
          .join(' ')
          .toLowerCase()

        return searchableText.includes(query)
      })
      .slice(0, 6)
  }, [searchQuery])

  const handleSearch = (value: string) => {
    setSearchQuery(value)
  }

  const handleSearchSubmit = () => {
    const query = searchQuery.trim().toLowerCase()

    if (!query) return

    const exactMatch = searchItems.find(
      (item) =>
        item.title.toLowerCase() === query ||
        item.keywords.includes(query),
    )

    const firstResult = exactMatch ?? filteredResults[0]

    if (firstResult) {
      navigate(firstResult.href)
      setSearchQuery('')
      setSearchFocused(false)
    }
  }

  const handleSearchResultClick = (href: string) => {
    navigate(href)
    setSearchQuery('')
    setSearchFocused(false)
  }

  const clearSearch = () => {
    setSearchQuery('')
  }

  return (
    <header className="sticky top-0 z-30 flex min-h-16 items-center gap-2 border-b border-border bg-background/70 px-3 backdrop-blur-xl sm:gap-3 sm:px-6">
      {/* Mobile menu */}
      <button
        onClick={onMenu}
        className="flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground lg:hidden"
        aria-label="Open navigation"
      >
        <Menu className="size-5" />
      </button>

      {/* SEARCH */}
      <div className="relative min-w-0 flex-1 sm:max-w-md">
        <Search className="pointer-events-none absolute left-3 top-1/2 z-10 size-4 -translate-y-1/2 text-muted-foreground" />

        <input
          type="search"
          value={searchQuery}
          onChange={(event) => handleSearch(event.target.value)}
          onFocus={() => setSearchFocused(true)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              handleSearchSubmit()
            }

            if (event.key === 'Escape') {
              setSearchFocused(false)
            }
          }}
          placeholder="Search lessons, gates, algorithms…"
          className="h-10 w-full min-w-0 rounded-xl border border-border bg-secondary/40 pl-9 pr-9 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-primary/40 focus:bg-secondary/70"
          aria-label="Search lessons, gates and algorithms"
        />

        {searchQuery && (
          <button
            type="button"
            onClick={clearSearch}
            className="absolute right-2 top-1/2 flex size-6 -translate-y-1/2 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
            aria-label="Clear search"
          >
            <X className="size-4" />
          </button>
        )}

        {/* Search results */}
        {searchFocused && searchQuery.trim() && (
          <div className="absolute left-0 right-0 top-12 z-50 overflow-hidden rounded-xl border border-border bg-background/95 shadow-2xl backdrop-blur-xl">
            {filteredResults.length > 0 ? (
              <div className="p-2">
                {filteredResults.map((item) => {
                  const Icon = item.icon

                  return (
                    <button
                      key={item.href}
                      type="button"
                      onMouseDown={(event) => {
                        event.preventDefault()
                      }}
                      onClick={() => handleSearchResultClick(item.href)}
                      className="flex w-full items-center gap-3 rounded-lg p-3 text-left transition-colors hover:bg-secondary"
                    >
                      <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                        <Icon className="size-4" />
                      </span>

                      <span className="min-w-0">
                        <span className="block text-sm font-medium text-foreground">
                          {item.title}
                        </span>

                        <span className="block truncate text-xs text-muted-foreground">
                          {item.description}
                        </span>
                      </span>
                    </button>
                  )
                })}
              </div>
            ) : (
              <div className="p-4 text-center">
                <p className="text-sm text-muted-foreground">
                  No results found
                </p>

                <p className="mt-1 text-xs text-muted-foreground/70">
                  Try searching for lessons, gates, circuits or algorithms.
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Right side */}
      <div className="ml-auto flex shrink-0 items-center gap-1.5 sm:gap-3">
        {/* Streak */}
        <Chip tone="amber" className="hidden sm:inline-flex">
          <Flame className="size-3.5" />
          {student.streak} day streak
        </Chip>

        {/* XP */}
        <Chip tone="cyan" className="hidden sm:inline-flex">
          <Zap className="size-3.5" />
          {student.xp.toLocaleString()} XP
        </Chip>

        {/* Theme */}
        <button
          onClick={toggleTheme}
          className="flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label={`Switch to ${
            theme === 'dark' ? 'light' : 'dark'
          } theme`}
          title={`Switch to ${
            theme === 'dark' ? 'light' : 'dark'
          } theme`}
        >
          {theme === 'dark' ? (
            <Sun className="size-5" />
          ) : (
            <Moon className="size-5" />
          )}
        </button>

        {/* Profile */}
        <div className="flex shrink-0 items-center gap-2.5 rounded-xl border border-border bg-secondary/40 py-1 pl-1 pr-2 sm:pr-3">
          <span className="flex size-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent text-sm font-bold text-primary-foreground">
            {displayName.charAt(0).toUpperCase()}
          </span>

          <div className="hidden leading-tight sm:block">
            <div className="text-sm font-medium">{displayName}</div>
            <div className="text-[11px] text-muted-foreground">
              {student.level}
            </div>
          </div>
        </div>

        {/* Logout */}
        <button
          onClick={logout}
          className="flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label="Log out"
          title="Log out"
        >
          <LogOut className="size-5" />
        </button>
      </div>
    </header>
  )
}