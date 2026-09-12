import { Routes, Route } from 'react-router-dom'
import { AppShell } from './components/app-shell'
import Dashboard from './pages/Dashboard'
import Learn from './pages/Learn'
import Lab from './pages/Lab'
import Copilot from './pages/Copilot'
import Challenges from './pages/Challenges'
import Progress from './pages/Progress'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Algorithms from "@/pages/Algorithms"
import Lesson from "@/pages/Lesson"

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/learn" element={<Learn />} />
        <Route path="/lab" element={<Lab />} />
        <Route path="/copilot" element={<Copilot />} />
        <Route path="/challenges" element={<Challenges />} />
        <Route path="/progress" element={<Progress />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<Dashboard />} />
        <Route path="/algorithms" element={<Algorithms />} />
        <Route path="/lesson" element={<Lesson />} />
      </Routes>
    </AppShell>
  )
}
