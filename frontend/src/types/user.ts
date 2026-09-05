/**
 * QuantumVerse AI — shared frontend data contracts.
 *
 * These interfaces describe the shape of the "current logged-in user" data.
 * The UI is built entirely against these types, so the backend team can later
 * return API responses in this shape without touching any page/component code.
 *
 * All fields are plain, JSON-serializable values (no functions, no React nodes,
 * icons are referenced by string key) so they can come straight from an API.
 */

export type SkillTone = 'cyan' | 'violet' | 'green' | 'amber'

/** Icon keys resolved to a real icon inside the UI (keeps data serializable). */
export type IconKey =
  | 'atom'
  | 'star'
  | 'zap'
  | 'flame'
  | 'trophy'
  | 'award'
  | 'medal'
  | 'crown'
  | 'brain'
  | 'target'
  | 'sparkles'
  | 'book'

/** The authenticated user's identity + profile info. */
export interface User {
  id: string
  name: string
  email: string
  avatarUrl?: string | null
  role: string
  joinedAt: string // ISO date string
}

/** High-level learning progress numbers for the current user. */
export interface UserProgress {
  overallProgress: number // 0-100
  level: number
  levelTitle: string
  xp: number
  nextLevelXp: number
  streakDays: number
  modulesCompleted: number
  totalModules: number
  challengesCompleted: number
  totalChallenges: number
  rank?: number | null
}

/** Mastery of a single quantum concept/skill. */
export interface SkillProgress {
  id: string
  name: string
  value: number // 0-100
  tone: SkillTone
}

/** A single earned or locked achievement/badge. */
export interface Achievement {
  id: string
  name: string
  description: string
  icon: IconKey
  earned: boolean
  earnedAt?: string | null // ISO date string when earned
  progress?: number | null // 0-100, optional progress toward a locked badge
}

export type ActivityKind = 'lesson' | 'challenge' | 'circuit' | 'badge'

/** A recent learning event in the user's timeline. */
export interface LearningActivity {
  id: string
  title: string
  meta: string
  time: string // human-friendly relative time from the backend
  kind: ActivityKind
  xp?: number | null
}

/** A single day of study time, used for the weekly activity chart. */
export interface DailyActivity {
  day: string
  minutes: number
}

/** A topic the learner is weak in and should revisit. */
export interface WeakTopic {
  id: string
  name: string
  accuracy: number // 0-100
}

/** A personalized next-step suggestion from the AI copilot. */
export interface Recommendation {
  id: string
  title: string
  description: string
  reason: string
  icon: IconKey
  href?: string
}

/**
 * The full data payload for the current user.
 * A backend endpoint (e.g. GET /me/dashboard) can return exactly this object.
 */
export interface CurrentUserData {
  user: User
  progress: UserProgress
  skills: SkillProgress[]
  achievements: Achievement[]
  activity: LearningActivity[]
  weeklyActivity: DailyActivity[]
  weakTopics: WeakTopic[]
  recommendations: Recommendation[]
}
