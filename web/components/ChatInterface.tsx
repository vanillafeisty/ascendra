'use client'
import { useState, useRef, useEffect, useCallback } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { Send, Plus, Menu, Zap } from 'lucide-react'
import MessageBubble from './MessageBubble'
import Sidebar from './Sidebar'
import { STARTER_PROMPTS, type Message, type Conversation } from '@/lib/types'
import { moderateInput } from '@/lib/moderation'

export default function ChatInterface() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Init first conversation
  useEffect(() => {
    const id = uuidv4()
    setActiveId(id)
    setConversations([{
      id, title: 'New conversation',
      messages: [], createdAt: new Date(), updatedAt: new Date()
    }])
  }, [])

  async function sendMessage(text?: string) {
    const content = (text ?? input).trim()
    if (!content || isLoading) return

    // Client-side moderation
    const mod = moderateInput(content)
    const userMsg: Message = { id: uuidv4(), role: 'user', content }
    let newMessages: Message[]

    if (mod.blocked) {
      const blockedReply: Message = { id: uuidv4(), role: 'assistant', content: mod.response! }
      newMessages = [...messages, userMsg, blockedReply]
      setMessages(newMessages)
      setInput('')
      return
    }

    newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput('')
    setIsLoading(true)

    // Update conversation title from first message
    if (messages.length === 0) {
      const title = content.slice(0, 50) + (content.length > 50 ? '…' : '')
      setConversations(prev => prev.map(c => c.id === activeId ? { ...c, title } : c))
    }

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role, content: m.content }))
        }),
      })

      const data = await res.json()
      const reply: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: data.message || 'Something went wrong. Please try again.'
      }
      const withReply = [...newMessages, reply]
      setMessages(withReply)
      setConversations(prev => prev.map(c =>
        c.id === activeId ? { ...c, messages: withReply, updatedAt: new Date() } : c
      ))
    } catch {
      setMessages(prev => [...prev, {
        id: uuidv4(), role: 'assistant',
        content: '⚠️ Cannot reach the backend. Make sure `python api.py` is running in the `backend/` folder.'
      }])
    } finally {
      setIsLoading(false)
    }
  }

  function newChat() {
    const id = uuidv4()
    setActiveId(id)
    setMessages([])
    setConversations(prev => [{
      id, title: 'New conversation',
      messages: [], createdAt: new Date(), updatedAt: new Date()
    }, ...prev])
    setSidebarOpen(false)
    setTimeout(() => textareaRef.current?.focus(), 100)
  }

  function switchConversation(id: string) {
    const conv = conversations.find(c => c.id === id)
    if (conv) {
      setActiveId(id)
      setMessages(conv.messages)
      setSidebarOpen(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  function autoResize(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setInput(e.target.value)
    const t = e.target
    t.style.height = 'auto'
    t.style.height = Math.min(t.scrollHeight, 160) + 'px'
  }

  const isEmpty = messages.length === 0

  return (
    <div className="flex h-screen bg-surface-0 overflow-hidden">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onNew={newChat}
        onSelect={switchConversation}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/60 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)} />
      )}

      <div className="flex flex-col flex-1 min-w-0">
        {/* Header */}
        <header className="flex items-center justify-between px-4 h-14 border-b border-white/5 flex-shrink-0">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)}
              className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/5 transition-colors md:hidden">
              <Menu size={18} />
            </button>
            <AscendraLogo />
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden sm:block text-xs font-mono text-white/25 px-2 py-1 border border-white/8 rounded-lg">
              Groq · llama-3.3-70b · free
            </span>
            <button onClick={newChat}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium
                text-white/50 hover:text-white hover:bg-white/5 transition-colors">
              <Plus size={14} /> New
            </button>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {isEmpty ? (
            <WelcomeScreen onPrompt={p => sendMessage(p)} />
          ) : (
            <div className="max-w-3xl mx-auto px-4 py-6 space-y-1">
              {messages.map(m => <MessageBubble key={m.id} message={m} />)}
              {isLoading && <ThinkingBubble />}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="flex-shrink-0 border-t border-white/5 bg-surface-0 px-4 py-4">
          <div className="max-w-3xl mx-auto">
            <div className="chat-input flex items-end gap-3 px-4 py-3 rounded-2xl
              bg-surface-3 border border-white/8 transition-all duration-200">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={autoResize}
                onKeyDown={handleKeyDown}
                placeholder="Ask Ascendra anything about your career…"
                rows={1}
                disabled={isLoading}
                className="flex-1 bg-transparent resize-none outline-none text-white
                  placeholder-white/25 text-sm leading-relaxed min-h-[24px] max-h-[160px]
                  overflow-y-auto"
                style={{ scrollbarWidth: 'none' }}
              />
              <button
                onClick={() => sendMessage()}
                disabled={!input.trim() || isLoading}
                className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center
                  bg-ascendra-500 disabled:opacity-30 disabled:cursor-not-allowed
                  hover:bg-ascendra-400 transition-all duration-200 hover:scale-105 active:scale-95">
                <Send size={14} className="text-white" />
              </button>
            </div>
            <p className="text-center text-white/20 text-xs mt-2">
              Review all automated LinkedIn/email actions before they send · Personal use only
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

function WelcomeScreen({ onPrompt }: { onPrompt: (p: string) => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-full px-4 py-12">
      <div className="text-center mb-10 animate-fade-in">
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="relative w-14 h-14 flex items-center justify-center">
            <div className="absolute inset-0 rounded-2xl bg-ascendra-500/15 border border-ascendra-500/30" />
            <svg width="28" height="28" viewBox="0 0 18 18" fill="none">
              <path d="M9 2L16 15H2L9 2Z" fill="none" stroke="#d4891e" strokeWidth="1.5" strokeLinejoin="round"/>
              <path d="M9 2L9 10" stroke="#d4891e" strokeWidth="1.5" strokeLinecap="round"/>
              <circle cx="9" cy="12" r="1.5" fill="#d4891e"/>
            </svg>
          </div>
        </div>
        <h1 className="font-display text-4xl font-bold text-white mb-3">
          How can I help you <span className="text-gold-gradient">rise today?</span>
        </h1>
        <p className="text-white/40 text-base max-w-md mx-auto mb-2">
          I'm Ascendra — your AI career co-pilot. Tell me your goal and I'll handle the rest.
        </p>
        <p className="text-white/20 text-xs font-mono">
          Powered by Groq (free) · llama-3.3-70b-versatile
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 w-full max-w-3xl animate-slide-up">
        {STARTER_PROMPTS.map(({ icon, title, prompt }) => (
          <button key={title} onClick={() => onPrompt(prompt)}
            className="group text-left p-4 rounded-xl border border-white/6 bg-surface-2
              hover:bg-surface-3 hover:border-ascendra-500/25 transition-all duration-200 hover:-translate-y-0.5">
            <div className="text-2xl mb-2">{icon}</div>
            <div className="text-sm font-semibold text-white/80 group-hover:text-white mb-1">{title}</div>
            <div className="text-xs text-white/35 line-clamp-2 leading-relaxed">{prompt.slice(0, 80)}…</div>
          </button>
        ))}
      </div>
    </div>
  )
}

function ThinkingBubble() {
  return (
    <div className="flex items-start gap-3 py-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-ascendra-500/15 border border-ascendra-500/30
        flex items-center justify-center mt-0.5">
        <Zap size={14} className="text-ascendra-400" />
      </div>
      <div className="flex items-center gap-1 px-4 py-3 rounded-2xl rounded-tl-none
        bg-surface-3 border border-white/6">
        <div className="thinking-dot w-1.5 h-1.5 rounded-full bg-ascendra-400" />
        <div className="thinking-dot w-1.5 h-1.5 rounded-full bg-ascendra-400" />
        <div className="thinking-dot w-1.5 h-1.5 rounded-full bg-ascendra-400" />
      </div>
    </div>
  )
}

function AscendraLogo() {
  return (
    <div className="flex items-center gap-2">
      <div className="w-7 h-7 rounded-lg bg-ascendra-500/15 border border-ascendra-500/30
        flex items-center justify-center">
        <svg width="14" height="14" viewBox="0 0 18 18" fill="none">
          <path d="M9 2L16 15H2L9 2Z" fill="none" stroke="#d4891e" strokeWidth="1.5" strokeLinejoin="round"/>
          <path d="M9 2L9 10" stroke="#d4891e" strokeWidth="1.5" strokeLinecap="round"/>
          <circle cx="9" cy="12" r="1.5" fill="#d4891e"/>
        </svg>
      </div>
      <span className="font-display font-semibold text-base text-white">Ascendra</span>
    </div>
  )
}
