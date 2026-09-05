
import { Link } from 'react-router-dom'
import { AuthLayout } from '@/components/auth/auth-layout'
import { SignupForm } from '@/components/auth/signup-form'

export default function SignupPage() {
  return (
    <AuthLayout
      title="Create your account"
      subtitle="Start learning, building, and simulating quantum computing."
      footer={
        <>
          {'Already have an account? '}
          <Link to="/login" className="font-semibold text-primary transition-opacity hover:opacity-80">
            Log in
          </Link>
        </>
      }
    >
      <SignupForm />
    </AuthLayout>
  )
}
