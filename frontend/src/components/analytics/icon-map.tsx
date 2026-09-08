import {
  Atom,
  Star,
  Zap,
  Flame,
  Trophy,
  Award,
  Medal,
  Crown,
  Brain,
  Target,
  Sparkles,
  BookOpen,
  type LucideIcon,
} from 'lucide-react'
import type { IconKey } from '@/types/user'

/** Resolves a serializable IconKey (from data/API) into a real Lucide icon. */
const ICONS: Record<IconKey, LucideIcon> = {
  atom: Atom,
  star: Star,
  zap: Zap,
  flame: Flame,
  trophy: Trophy,
  award: Award,
  medal: Medal,
  crown: Crown,
  brain: Brain,
  target: Target,
  sparkles: Sparkles,
  book: BookOpen,
}

export function resolveIcon(key: IconKey): LucideIcon {
  return ICONS[key] ?? Atom
}
