'use client'
import { useState, useRef, useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { Send, Plus, MessageSquare, TrendingUp, Home, Menu, X, ChevronRight } from 'lucide-react'
import MessageBubble from './MessageBubble'
import { STARTERS } from '@/lib/constants'
import type { Message, Conversation } from '@/lib/types'

export default function ChatInterface() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId]           = useState('')
  const [messages, setMessages]           = useState<Message[]>([])
  const [input, setInput]                 = useState('')
  const [loading, setLoading]             = useState(false)
  const [sidebarOpen, setSidebarOpen]     = useState(false)
  const [linkedinStatus, setLinkedinStatus] = useState<'unknown'|'checking'|'ok'|'error'>('unknown')
  const [linkedinName, setLinkedinName]   = useState('')
  const bottomRef  = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const id = uuidv4()
    setActiveId(id)
    setConversations([{ id, title:'New conversation', messages:[], createdAt:new Date(), updatedAt:new Date() }])
    // Check LinkedIn on mount
    checkLinkedIn()
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior:'smooth' })
  }, [messages, loading])

  async function checkLinkedIn() {
    setLinkedinStatus('checking')
    try {
      const res = await fetch('http://localhost:8000/api/linkedin/test')
      const data = await res.json()
      if (data.connected) {
        setLinkedinStatus('ok')
        setLinkedinName(data.profile?.name || 'Connected')
      } else {
        setLinkedinStatus('error')
      }
    } catch {
      setLinkedinStatus('error')
    }
  }

  async function send(text?: string) {
    const content = (text ?? input).trim()
    if (!content || loading) return

    const userMsg: Message = { id: uuidv4(), role:'user', content }
    const next = [...messages, userMsg]
    setMessages(next)
    setInput('')
    setLoading(true)

    if (messages.length === 0) {
      const title = content.slice(0,48) + (content.length > 48 ? '…' : '')
      setConversations(p => p.map(c => c.id === activeId ? { ...c, title } : c))
    }

    try {
      const res = await fetch('/api/chat', {
        method:'POST',
        headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify({ messages: next.map(m=>({ role:m.role, content:m.content })) })
      })
      const data = await res.json()
      const reply: Message = { id:uuidv4(), role:'assistant', content: data.message || 'Something went wrong.' }
      const withReply = [...next, reply]
      setMessages(withReply)
      setConversations(p => p.map(c => c.id===activeId ? { ...c, messages:withReply, updatedAt:new Date() } : c))
    } catch {
      setMessages(p => [...p, { id:uuidv4(), role:'assistant', content:'⚠️ Cannot reach backend. Run `python api.py` in the backend folder.' }])
    } finally {
      setLoading(false)
    }
  }

  function newChat() {
    const id = uuidv4()
    setActiveId(id)
    setMessages([])
    setConversations(p => [{ id, title:'New conversation', messages:[], createdAt:new Date(), updatedAt:new Date() }, ...p])
    setSidebarOpen(false)
    setTimeout(() => textareaRef.current?.focus(), 80)
  }

  function switchConv(id: string) {
    const c = conversations.find(x => x.id === id)
    if (c) { setActiveId(id); setMessages(c.messages); setSidebarOpen(false) }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  function resize(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setInput(e.target.value)
    const t = e.target; t.style.height = 'auto'
    t.style.height = Math.min(t.scrollHeight, 150) + 'px'
  }

  const isEmpty = messages.length === 0

  return (
    <div className="flex h-screen" style={{ background:'var(--cream)' }}>

      {/* ── Sidebar ─────────────────────────────────────────── */}
      <aside className={`
        fixed md:relative inset-y-0 left-0 z-40 w-64 flex flex-col
        transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `} style={{ background:'#fff', borderRight:'1px solid var(--border)' }}>

        {/* Logo */}
        <div className="flex items-center justify-between px-5 h-14"
          style={{ borderBottom:'1px solid var(--border)' }}>
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg flex items-center justify-center"
              style={{ background:'var(--sage-light)', border:'1px solid var(--border-sage)' }}>
              <TrendingUp size={14} style={{ color:'var(--sage)' }} />
            </div>
            <span className="font-display font-semibold text-base tracking-tight"
              style={{ color:'var(--stone-900)' }}>Ascendra</span>
          </div>
          <button onClick={() => setSidebarOpen(false)} className="md:hidden p-1 rounded-lg hover:bg-stone-100 transition-colors">
            <X size={16} style={{ color:'var(--stone-500)' }} />
          </button>
        </div>

        {/* LinkedIn status pill */}
        <div className="px-4 py-3">
          <button onClick={checkLinkedIn}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-colors"
            style={{
              background: linkedinStatus === 'ok' ? 'var(--sage-light)' : linkedinStatus === 'error' ? '#FEF3F2' : 'var(--stone-100)',
              border: `1px solid ${linkedinStatus === 'ok' ? 'var(--border-sage)' : linkedinStatus === 'error' ? 'rgba(239,68,68,0.2)' : 'var(--border)'}`,
              color: linkedinStatus === 'ok' ? 'var(--sage-600,#4E6549)' : linkedinStatus === 'error' ? '#B91C1C' : 'var(--stone-500)',
            }}>
            <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
              linkedinStatus === 'ok' ? 'bg-green-500' :
              linkedinStatus === 'error' ? 'bg-red-400' :
              linkedinStatus === 'checking' ? 'bg-amber-400 animate-pulse' : 'bg-stone-300'
            }`} />
            {linkedinStatus === 'ok'       ? `LinkedIn · ${linkedinName}` :
             linkedinStatus === 'error'    ? 'LinkedIn · Not connected' :
             linkedinStatus === 'checking' ? 'LinkedIn · Checking...' :
                                             'LinkedIn · Click to test'}
          </button>
        </div>

        {/* New chat */}
        <div className="px-3 pb-2">
          <button onClick={newChat}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-colors hover:bg-stone-50"
            style={{ color:'var(--stone-500)', border:'1px dashed var(--border)' }}>
            <Plus size={15} /> New conversation
          </button>
        </div>

        {/* Conversations */}
        <div className="flex-1 overflow-y-auto px-3 pb-4">
          {conversations.length > 0 && (
            <>
              <div className="px-2 py-2 text-xs font-semibold uppercase tracking-widest"
                style={{ color:'var(--stone-400,#B8B2AB)', fontFamily:'var(--font-mono)' }}>
                Recent
              </div>
              {conversations.map(c => (
                <button key={c.id} onClick={() => switchConv(c.id)}
                  className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-left text-xs mb-0.5 transition-colors"
                  style={{
                    background: c.id === activeId ? 'var(--sage-light)' : 'transparent',
                    border: c.id === activeId ? '1px solid var(--border-sage)' : '1px solid transparent',
                    color: c.id === activeId ? 'var(--sage-600,#4E6549)' : 'var(--stone-500)',
                  }}>
                  <MessageSquare size={13} className="flex-shrink-0 opacity-60" />
                  <span className="truncate">{c.title}</span>
                </button>
              ))}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-3" style={{ borderTop:'1px solid var(--border)' }}>
          <a href="/"
            className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs transition-colors hover:bg-stone-50"
            style={{ color:'var(--stone-400,#B8B2AB)' }}>
            <Home size={13} /> Back to home
          </a>
          <p className="text-xs mt-2 px-3" style={{ color:'var(--stone-300, #D6D2CD)', fontFamily:'var(--font-mono)' }}>
            Groq · llama-3.3-70b · free
          </p>
        </div>
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/20 z-30 md:hidden backdrop-blur-sm"
          onClick={() => setSidebarOpen(false)} />
      )}

      {/* ── Main ────────────────────────────────────────────── */}
      <div className="flex flex-col flex-1 min-w-0">

        {/* Header */}
        <header className="flex items-center justify-between px-5 h-14 flex-shrink-0"
          style={{ borderBottom:'1px solid var(--border)', background:'#fff' }}>
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)}
              className="p-1.5 rounded-lg transition-colors hover:bg-stone-100 md:hidden">
              <Menu size={18} style={{ color:'var(--stone-500)' }} />
            </button>
            <span className="font-display font-semibold text-base tracking-tight"
              style={{ color:'var(--stone-900)' }}>Ascendra</span>
          </div>
          <button onClick={newChat}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors hover:bg-stone-50"
            style={{ color:'var(--stone-500)' }}>
            <Plus size={14} /> New
          </button>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto" style={{ background:'var(--cream)' }}>
          {isEmpty ? (
            <WelcomeScreen onPrompt={send} linkedinStatus={linkedinStatus} linkedinName={linkedinName} onCheckLinkedIn={checkLinkedIn} />
          ) : (
            <div className="max-w-2xl mx-auto px-4 py-6 space-y-1">
              {messages.map(m => <MessageBubble key={m.id} message={m} />)}
              {loading && <ThinkingBubble />}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="flex-shrink-0 px-4 py-4" style={{ borderTop:'1px solid var(--border)', background:'#fff' }}>
          <div className="max-w-2xl mx-auto">
            <div className="input-field flex items-end gap-3 px-4 py-3 rounded-2xl transition-all"
              style={{ background:'var(--cream)', border:'1px solid var(--stone-200, #EAE8E5)' }}>
              <textarea
                ref={textareaRef}
                value={input}
                onChange={resize}
                onKeyDown={handleKey}
                placeholder="Ask Ascendra anything about your career…"
                rows={1}
                disabled={loading}
                className="flex-1 bg-transparent resize-none outline-none text-sm leading-relaxed"
                style={{ color:'var(--stone-900)', minHeight:'24px', maxHeight:'150px',
                         fontFamily:'var(--font-body)', scrollbarWidth:'none' }}
              />
              <button onClick={() => send()} disabled={!input.trim() || loading}
                className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-all hover:opacity-90 active:scale-95 disabled:opacity-30"
                style={{ background:'var(--sage)', color:'var(--cream)' }}>
                <Send size={14} />
              </button>
            </div>
            <p className="text-center text-xs mt-2" style={{ color:'var(--stone-300, #D6D2CD)', fontFamily:'var(--font-mono)' }}>
              Review all LinkedIn & email actions before they send · Personal use only
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

function WelcomeScreen({ onPrompt, linkedinStatus, linkedinName, onCheckLinkedIn }:
  { onPrompt:(p:string)=>void; linkedinStatus:string; linkedinName:string; onCheckLinkedIn:()=>void }) {
  return (
    <div className="flex flex-col items-center justify-start min-h-full px-4 py-10 max-w-2xl mx-auto">
      {/* LinkedIn status banner */}
      <div className="w-full mb-8 rounded-2xl p-4 flex items-center justify-between"
        style={{
          background: linkedinStatus === 'ok' ? 'var(--sage-light)' : linkedinStatus === 'error' ? '#FEF9F9' : 'var(--stone-100)',
          border: `1px solid ${linkedinStatus === 'ok' ? 'var(--border-sage)' : linkedinStatus === 'error' ? 'rgba(239,68,68,0.15)' : 'var(--border)'}`,
        }}>
        <div className="flex items-center gap-3">
          <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${
            linkedinStatus === 'ok' ? 'bg-green-500' :
            linkedinStatus === 'error' ? 'bg-red-400' :
            linkedinStatus === 'checking' ? 'bg-amber-400 animate-pulse' : 'bg-stone-300'
          }`} />
          <div>
            <p className="text-sm font-semibold"
              style={{ color: linkedinStatus === 'ok' ? 'var(--sage-600,#4E6549)' : 'var(--stone-700)' }}>
              {linkedinStatus === 'ok'    ? `✅ LinkedIn connected as ${linkedinName}` :
               linkedinStatus === 'error' ? '⚠️ LinkedIn not connected' :
               linkedinStatus === 'checking' ? 'Checking LinkedIn…' : 'LinkedIn status unknown'}
            </p>
            <p className="text-xs mt-0.5"
              style={{ color:'var(--stone-500)', fontFamily:'var(--font-mono)' }}>
              {linkedinStatus === 'ok'
                ? 'Connection requests & messages will send from your account'
                : 'Add LINKEDIN_EMAIL + LINKEDIN_PASSWORD to backend/.env'}
            </p>
          </div>
        </div>
        {linkedinStatus !== 'ok' && (
          <button onClick={onCheckLinkedIn}
            className="text-xs px-3 py-1.5 rounded-lg font-medium transition-colors hover:opacity-80"
            style={{ background:'var(--sage)', color:'var(--cream)' }}>
            Test Again
          </button>
        )}
      </div>

      {/* Greeting */}
      <div className="text-center mb-8">
        <h1 className="font-display font-semibold mb-2"
          style={{ fontSize:'clamp(1.6rem,4vw,2.4rem)', color:'var(--stone-900)', letterSpacing:'-0.02em' }}>
          How can I help you rise today?
        </h1>
        <p className="text-sm" style={{ color:'var(--stone-500)' }}>
          Tell me your goal — I'll handle the rest.
        </p>
      </div>

      {/* Starter prompts */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-2 gap-3">
        {STARTERS.map(({ icon, title, prompt }) => (
          <button key={title} onClick={() => onPrompt(prompt)}
            className="card-hover group text-left p-4 rounded-xl transition-all"
            style={{ background:'#fff', border:'1px solid var(--border)', boxShadow:'var(--shadow-sm)' }}>
            <div className="flex items-start gap-3">
              <span className="text-xl mt-0.5">{icon}</span>
              <div>
                <p className="text-sm font-semibold mb-1 group-hover:text-sage-500 transition-colors"
                  style={{ color:'var(--stone-800,#3A3733)' }}>{title}</p>
                <p className="text-xs leading-relaxed" style={{ color:'var(--stone-400,#B8B2AB)' }}>
                  {prompt.slice(0,75)}…
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

function ThinkingBubble() {
  return (
    <div className="flex items-start gap-3 py-3 animate-fade-in">
      <AvatarIcon />
      <div className="flex items-center gap-1.5 px-4 py-3 rounded-2xl rounded-tl-sm"
        style={{ background:'#fff', border:'1px solid var(--border)' }}>
        <div className="dot-1 w-1.5 h-1.5 rounded-full" style={{ background:'var(--sage)' }} />
        <div className="dot-2 w-1.5 h-1.5 rounded-full" style={{ background:'var(--sage)' }} />
        <div className="dot-3 w-1.5 h-1.5 rounded-full" style={{ background:'var(--sage)' }} />
      </div>
    </div>
  )
}

export function AvatarIcon() {
  return (
    <div className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center mt-0.5"
      style={{ background:'var(--sage-light)', border:'1px solid var(--border-sage)' }}>
      <TrendingUp size={14} style={{ color:'var(--sage)' }} />
    </div>
  )
}
