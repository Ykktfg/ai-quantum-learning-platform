
import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { User, AtSign, Mail, Lock, UserPlus, Loader2, AlertCircle } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'
import { AuthField } from '@/components/auth/auth-field'

interface FieldErrors {
  name?: string
  username?: string
  email?: string
  password?: string
  confirmPassword?: string
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function SignupForm() {
  const navigate = useNavigate()
  const { signup } = useAuth()

  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [errors, setErrors] = useState<FieldErrors>({})
  const [formError, setFormError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  function validate(): FieldErrors {
    const next: FieldErrors = {}
    if (!name.trim()) next.name = 'Please enter your name.'
    if (!username.trim()) next.username = 'Please choose a username.'
    else if (username.trim().length < 3) next.username = 'Username must be at least 3 characters.'
    if (!email.trim()) next.email = 'Please enter your email.'
    else if (!EMAIL_RE.test(email.trim())) next.email = 'Enter a valid email address.'
    if (!password) next.password = 'Please create a password.'
    else if (password.length < 8) next.password = 'Password must be at least 8 characters.'
    if (confirmPassword !== password) next.confirmPassword = 'Passwords do not match.'
    return next
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setFormError(null)
    const nextErrors = validate()
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    setSubmitting(true)
    try {
      await signup({ name, username, email, password })
      navigate('/')
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Unable to create your account. Please try again.')
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      {formError ? (
        <div className="flex items-start gap-2 rounded-xl border border-destructive/40 bg-destructive/10 px-3 py-2.5 text-sm text-destructive">
          <AlertCircle className="mt-0.5 size-4 shrink-0" />
          <span>{formError}</span>
        </div>
      ) : null}

      <AuthField
        label="Full name"
        icon={<User className="size-4" />}
        placeholder="Ada Lovelace"
        autoComplete="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        error={errors.name}
        required
      />

      <AuthField
        label="Username"
        icon={<AtSign className="size-4" />}
        placeholder="ada"
        autoComplete="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        error={errors.username}
        required
      />

      <AuthField
        label="Email"
        icon={<Mail className="size-4" />}
        type="email"
        placeholder="ada@quantumverse.ai"
        autoComplete="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={errors.email}
        required
      />

      <AuthField
        label="Password"
        icon={<Lock className="size-4" />}
        type="password"
        placeholder="At least 8 characters"
        autoComplete="new-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        required
      />

      <AuthField
        label="Confirm password"
        icon={<Lock className="size-4" />}
        type="password"
        placeholder="Re-enter your password"
        autoComplete="new-password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        error={errors.confirmPassword}
        required
      />

      <button
        type="submit"
        disabled={submitting}
        className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-accent text-sm font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {submitting ? (
          <>
            <Loader2 className="size-4 animate-spin" />
            Creating account…
          </>
        ) : (
          <>
            <UserPlus className="size-4" />
            Create account
          </>
        )}
      </button>
    </form>
  )
}
