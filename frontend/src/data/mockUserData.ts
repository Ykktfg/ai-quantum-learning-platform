/**
 * TEMPORARY mock data for the "current user".
 *
 * This is the ONLY place demo values live. Every Progress/Profile component
 * reads its data through `useUserData()` (see hooks/use-user-data.ts), which
 * currently returns this object. To go live, the backend team only needs to
 * replace the resolver in that hook with a real fetch that returns a
 * `CurrentUserData` payload — no UI changes required.
 */

import type { CurrentUserData } from '@/types/user'

export const mockCurrentUserData: CurrentUserData = {
  user: {
    id: 'usr_aarav_01',
    name: 'Aarav Sharma',
    email: 'aarav.sharma@quantumverse.ai',
    avatarUrl: null,
    role: 'Student',
    joinedAt: '2025-01-14',
  },

  progress: {
    overallProgress: 68,
    level: 7,
    levelTitle: 'Quantum Explorer',
    xp: 4820,
    nextLevelXp: 6000,
    streakDays: 12,
    modulesCompleted: 24,
    totalModules: 42,
    challengesCompleted: 9,
    totalChallenges: 18,
    rank: 3,
  },

  skills: [
    { id: 'fundamentals', name: 'Quantum Fundamentals', value: 88, tone: 'cyan' },
    { id: 'superposition', name: 'Superposition', value: 82, tone: 'cyan' },
    { id: 'gates', name: 'Quantum Gates', value: 76, tone: 'green' },
    { id: 'entanglement', name: 'Entanglement', value: 48, tone: 'violet' },
    { id: 'circuits', name: 'Circuit Design', value: 64, tone: 'green' },
    { id: 'algorithms', name: 'Quantum Algorithms', value: 35, tone: 'amber' },
  ],

  achievements: [
    { id: 'first-qubit', name: 'First Qubit', description: 'Completed your first lesson', icon: 'atom', earned: true, earnedAt: '2025-01-15' },
    { id: 'superposition-adept', name: 'Superposition Adept', description: 'Mastered superposition', icon: 'star', earned: true, earnedAt: '2025-02-02' },
    { id: 'bell-ringer', name: 'Bell Ringer', description: 'Built your first Bell State', icon: 'zap', earned: true, earnedAt: '2025-02-10' },
    { id: 'streak-keeper', name: 'Streak Keeper', description: '7-day learning streak', icon: 'flame', earned: true, earnedAt: '2025-02-18' },
    { id: 'circuit-architect', name: 'Circuit Architect', description: 'Built 10 circuits', icon: 'trophy', earned: true, earnedAt: '2025-03-01' },
    { id: 'entanglement-master', name: 'Entanglement Master', description: 'Complete all entanglement lessons', icon: 'award', earned: false, progress: 48 },
    { id: 'algorithm-wizard', name: 'Algorithm Wizard', description: 'Solve Grover & Shor challenges', icon: 'brain', earned: false, progress: 20 },
    { id: 'quantum-sage', name: 'Quantum Sage', description: 'Reach Level 10', icon: 'crown', earned: false, progress: 70 },
  ],

  activity: [
    { id: 'a1', title: 'Completed "Hadamard Gate" lesson', meta: 'Quantum Gates', time: '2h ago', kind: 'lesson', xp: 120 },
    { id: 'a2', title: 'Solved "Create Superposition" challenge', meta: 'Challenge', time: '5h ago', kind: 'challenge', xp: 200 },
    { id: 'a3', title: 'Built a 3-qubit Bell circuit', meta: 'Circuit Lab', time: 'Yesterday', kind: 'circuit', xp: 80 },
    { id: 'a4', title: 'Earned "Entanglement Novice" badge', meta: 'Achievement', time: '2 days ago', kind: 'badge' },
    { id: 'a5', title: 'Completed "Bloch Sphere" lesson', meta: 'Qubits', time: '3 days ago', kind: 'lesson', xp: 100 },
  ],

  weeklyActivity: [
    { day: 'Mon', minutes: 45 },
    { day: 'Tue', minutes: 30 },
    { day: 'Wed', minutes: 65 },
    { day: 'Thu', minutes: 20 },
    { day: 'Fri', minutes: 80 },
    { day: 'Sat', minutes: 55 },
    { day: 'Sun', minutes: 40 },
  ],

  weakTopics: [
    { id: 'w1', name: 'Quantum Algorithms', accuracy: 42 },
    { id: 'w2', name: 'Phase Estimation', accuracy: 51 },
    { id: 'w3', name: 'Entanglement', accuracy: 58 },
  ],

  recommendations: [
    { id: 'r1', title: 'Review Grover Search', description: 'Your algorithm accuracy is at 42%. A focused refresher will help.', reason: 'Weak topic', icon: 'target', href: '/learn' },
    { id: 'r2', title: 'Practice Phase Kickback', description: 'Unlock the "Phase Master" badge with a controlled-Z challenge.', reason: 'Next badge', icon: 'zap', href: '/challenges' },
    { id: 'r3', title: 'Build a GHZ State', description: 'Extend your entanglement skills to three qubits in the lab.', reason: 'Skill growth', icon: 'sparkles', href: '/lab' },
  ],
}

/**
 * An "empty" new-user payload. Useful for previewing zero-state UI and for
 * testing that every component degrades gracefully when a brand-new account
 * has no progress yet. Not wired in by default.
 */
export const emptyNewUserData: CurrentUserData = {
  user: {
    id: 'usr_new',
    name: 'New Learner',
    email: 'new.learner@quantumverse.ai',
    avatarUrl: null,
    role: 'Student',
    joinedAt: new Date().toISOString().slice(0, 10),
  },
  progress: {
    overallProgress: 0,
    level: 1,
    levelTitle: 'Quantum Novice',
    xp: 0,
    nextLevelXp: 500,
    streakDays: 0,
    modulesCompleted: 0,
    totalModules: 42,
    challengesCompleted: 0,
    totalChallenges: 18,
    rank: null,
  },
  skills: [],
  achievements: [],
  activity: [],
  weeklyActivity: [],
  weakTopics: [],
  recommendations: [],
}
