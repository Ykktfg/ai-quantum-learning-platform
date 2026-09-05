
import { useState, useRef, useEffect } from 'react'
import { useChat } from '@ai-sdk/react'
import { DefaultChatTransport } from 'ai'
import { Send, Sparkles, Atom, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { GlassCard } from '@/components/quantum-ui'
import { suggestedQuestions } from '@/lib/data'
import { cn } from '@/lib/utils'

export function Copilot() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  })
  const [input, setInput] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)
  const busy = status === 'submitted' || status === 'streaming'

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  function submit(text: string) {
    const value = text.trim()
    if (!value || busy) return
    sendMessage({ text: value })
    setInput('')
  }

  return (
    <GlassCard className="flex flex-1 flex-col overflow-hidden">
      {/* messages */}
      <div ref={scrollRef} className="flex-1 space-y-5 overflow-y-auto p-4 sm:p-6">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 ring-1 ring-primary/25">
              <Atom className="size-8 text-primary" style={{ animation: 'orbit-spin 14s linear infinite' }} />
            </span>
            <h2 className="mt-4 text-balance text-lg font-semibold">Ask me anything about quantum computing</h2>
            <p className="mt-1 max-w-sm text-pretty text-sm text-muted-foreground">
              I can explain concepts, help debug your circuits, and guide you through challenges.
            </p>
            <div className="mt-6 grid w-full max-w-lg gap-2 sm:grid-cols-2">
              {suggestedQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => submit(q)}
                  className="rounded-xl border border-border bg-secondary/40 p-3 text-left text-sm transition-colors hover:border-primary/40 hover:bg-secondary/70"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((m) => (
            <div key={m.id} className={cn('flex gap-3', m.role === 'user' && 'flex-row-reverse')}>
              <span
                className={cn(
                  'flex size-8 shrink-0 items-center justify-center rounded-lg ring-1',
                  m.role === 'user'
                    ? 'bg-secondary text-foreground ring-border'
                    : 'bg-accent/15 text-accent ring-accent/25',
                )}
              >
                {m.role === 'user' ? <User className="size-4" /> : <Sparkles className="size-4" />}
              </span>
              <div
                className={cn(
                  'max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm leading-relaxed',
                  m.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-secondary/60 text-foreground',
                )}
              >
                {m.parts.map((part, i) => (part.type === 'text' ? <span key={i}>{part.text}</span> : null))}
              </div>
            </div>
          ))
        )}

        {status === 'submitted' ? (
          <div className="flex gap-3">
            <span className="flex size-8 items-center justify-center rounded-lg bg-accent/15 text-accent ring-1 ring-accent/25">
              <Sparkles className="size-4" />
            </span>
            <div className="flex items-center gap-1 rounded-2xl bg-secondary/60 px-4 py-3">
              <Dot /> <Dot delay="0.15s" /> <Dot delay="0.3s" />
            </div>
          </div>
        ) : null}
      </div>

      {/* input */}
      <div className="border-t border-border p-3 sm:p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            submit(input)
          }}
          className="flex items-end gap-2"
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing && e.keyCode !== 229) {
                e.preventDefault()
                submit(input)
              }
            }}
            rows={1}
            placeholder="Ask about superposition, gates, algorithms…"
            className="max-h-32 min-h-[44px] flex-1 resize-none rounded-xl border border-border bg-secondary/40 px-4 py-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-primary/40 focus:bg-secondary/70"
          />
          <Button type="submit" size="icon" className="size-11 shrink-0 rounded-xl" disabled={busy || !input.trim()}>
            <Send className="size-4" />
          </Button>
        </form>
      </div>
    </GlassCard>
  )
}

function Dot({ delay = '0s' }: { delay?: string }) {
  return <span className="size-2 rounded-full bg-accent" style={{ animation: `quantum-pulse 1s ease-in-out ${delay} infinite` }} />
}
