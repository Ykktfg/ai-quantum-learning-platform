export const student = {
  name: 'Aarav Sharma',
  level: 'Quantum Explorer · Level 7',
  streak: 12,
  xp: 4820,
  nextLevelXp: 6000,
  overallProgress: 68,
  lessonsCompleted: 24,
  totalLessons: 42,
  challengesCompleted: 9,
  totalChallenges: 18,
}

export const skillProfile = [
  { name: 'Superposition', value: 82, tone: 'cyan' as const },
  { name: 'Quantum Gates', value: 76, tone: 'cyan' as const },
  { name: 'Entanglement', value: 48, tone: 'violet' as const },
  { name: 'Quantum Algorithms', value: 35, tone: 'amber' as const },
  { name: 'Circuit Design', value: 64, tone: 'green' as const },
]

export const recentActivity = [
  { title: 'Completed "Hadamard Gate" lesson', meta: 'Quantum Gates · +120 XP', time: '2h ago', kind: 'lesson' as const },
  { title: 'Solved "Create Superposition" challenge', meta: 'Challenge · +200 XP', time: '5h ago', kind: 'challenge' as const },
  { title: 'Built a 3-qubit Bell circuit', meta: 'Circuit Lab', time: 'Yesterday', kind: 'circuit' as const },
  { title: 'Earned "Entanglement Novice" badge', meta: 'Achievement', time: '2 days ago', kind: 'badge' as const },
]

export const upcomingChallenges = [
  { title: 'Quantum Teleportation', difficulty: 'Hard', xp: 500 },
  { title: 'Grover Search (2 qubit)', difficulty: 'Hard', xp: 450 },
  { title: 'Deutsch–Jozsa Oracle', difficulty: 'Medium', xp: 320 },
]

export const modules = [
  {
    id: 'intro',
    title: 'Introduction to Quantum Computing',
    description: 'Why quantum matters and how it differs from classical computing.',
    difficulty: 'Beginner',
    progress: 100,
    time: '25 min',
    lessons: 6,
  },
  {
    id: 'qubits',
    title: 'Qubits',
    description: 'The Bloch sphere, quantum states and measurement basics.',
    difficulty: 'Beginner',
    progress: 100,
    time: '35 min',
    lessons: 7,
  },
  {
    id: 'superposition',
    title: 'Superposition',
    description: 'Placing qubits in |0⟩ + |1⟩ states with the Hadamard gate.',
    difficulty: 'Beginner',
    progress: 82,
    time: '40 min',
    lessons: 8,
  },
  {
    id: 'gates',
    title: 'Quantum Gates',
    description: 'Pauli, phase, and controlled gates that transform qubits.',
    difficulty: 'Intermediate',
    progress: 76,
    time: '55 min',
    lessons: 10,
  },
  {
    id: 'entanglement',
    title: 'Entanglement',
    description: 'Bell states, correlations and spooky action at a distance.',
    difficulty: 'Intermediate',
    progress: 48,
    time: '50 min',
    lessons: 9,
  },
  {
    id: 'circuits',
    title: 'Quantum Circuits',
    description: 'Composing gates into meaningful, measurable programs.',
    difficulty: 'Intermediate',
    progress: 30,
    time: '45 min',
    lessons: 8,
  },
  {
    id: 'algorithms',
    title: 'Quantum Algorithms',
    description: 'Deutsch–Jozsa, Grover, and Shor at an intuitive level.',
    difficulty: 'Advanced',
    progress: 12,
    time: '70 min',
    lessons: 11,
  },
]

export const challenges = [
  {
    id: 1,
    title: 'Create Superposition',
    goal: 'Create a qubit with a 50/50 probability of measuring 0 or 1.',
    difficulty: 'Beginner',
    xp: 200,
    status: 'completed' as const,
    badge: 'Superposition Adept',
  },
  {
    id: 2,
    title: 'Create Entanglement',
    goal: 'Create a Bell State by entangling two qubits.',
    difficulty: 'Intermediate',
    xp: 350,
    status: 'in-progress' as const,
    badge: 'Bell Ringer',
  },
  {
    id: 3,
    title: 'Quantum Teleportation',
    goal: 'Implement the basic quantum teleportation protocol.',
    difficulty: 'Advanced',
    xp: 500,
    status: 'locked' as const,
    badge: 'Teleporter',
  },
  {
    id: 4,
    title: 'Phase Kickback',
    goal: 'Demonstrate phase kickback using a controlled-Z gate.',
    difficulty: 'Intermediate',
    xp: 300,
    status: 'available' as const,
    badge: 'Phase Master',
  },
  {
    id: 5,
    title: 'Grover Search',
    goal: 'Find a marked item in an unsorted 2-qubit database.',
    difficulty: 'Advanced',
    xp: 450,
    status: 'locked' as const,
    badge: 'Search Wizard',
  },
  {
    id: 6,
    title: 'GHZ State',
    goal: 'Entangle three qubits into a GHZ state.',
    difficulty: 'Advanced',
    xp: 420,
    status: 'available' as const,
    badge: 'Triple Threat',
  },
]

export const leaderboard = [
  { rank: 1, name: 'Meera Nair', xp: 9840, you: false },
  { rank: 2, name: 'Rohan Gupta', xp: 8120, you: false },
  { rank: 3, name: 'Aarav Sharma', xp: 4820, you: true },
  { rank: 4, name: 'Diya Patel', xp: 4510, you: false },
  { rank: 5, name: 'Kabir Singh', xp: 3990, you: false },
]

export const weeklyActivity = [
  { day: 'Mon', minutes: 45 },
  { day: 'Tue', minutes: 30 },
  { day: 'Wed', minutes: 65 },
  { day: 'Thu', minutes: 20 },
  { day: 'Fri', minutes: 80 },
  { day: 'Sat', minutes: 55 },
  { day: 'Sun', minutes: 40 },
]

export const weakTopics = [
  { name: 'Quantum Algorithms', accuracy: 42 },
  { name: 'Entanglement', accuracy: 58 },
  { name: 'Phase Estimation', accuracy: 51 },
]

export const suggestedQuestions = [
  'What is a Bell State and how do I build one?',
  'Explain the difference between the X and Z gates.',
  'Why does measurement collapse superposition?',
  'How does the CNOT gate create entanglement?',
]
