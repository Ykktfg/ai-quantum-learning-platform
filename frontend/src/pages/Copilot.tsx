import { Bot } from 'lucide-react'
import { Chip } from '@/components/quantum-ui'
import { Copilot } from '@/components/copilot'

export default function CopilotPage() {
  return (
    <div className="mx-auto flex h-[calc(100vh-8rem)] max-w-4xl flex-col">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-accent">
            <Bot className="size-5" />
            <span className="text-sm font-medium tracking-wide">POWERED BY AI</span>
          </div>
          <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">AI Quantum Copilot</h1>
        </div>
        <Chip tone="violet" className="w-fit">
          Live assistant
        </Chip>
      </div>
      <Copilot />
    </div>
  )
}
