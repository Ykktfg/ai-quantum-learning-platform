
import { Link } from 'react-router-dom'
import { AuthLayout } from '@/components/auth/auth-layout'
import { LoginForm } from '@/components/auth/login-form'

export default function LoginPage() {
  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Log in to continue your quantum journey."
      footer={
        <>
          {"Don't have an account? "}
          <Link to="/signup" className="font-semibold text-primary transition-opacity hover:opacity-80">
            Sign up
          </Link>
        </>
      }
    >
      <LoginForm />
    </AuthLayout>
  )
}
