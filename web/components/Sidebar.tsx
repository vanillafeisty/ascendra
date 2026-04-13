'use client'
import { MessageSquare, Plus, X, Home } from 'lucide-react'
import Link from 'next/link'
import type { Conversation } from '@/lib/types'

interface Props {
  conversations: Conversation[]
  activeId: string
  onNew: () => void
  onSelect: (id: string) => void
  isOpen: boolean
  onClose: () => void
}

export default function Sidebar({ conversations, activeId, onNew, onSelect, isOpen, onClose }: Props) {
  return (
    <aside className={`
      fixed md:relative inset-y-0 left-0 z-40
      w-64 flex flex-col
      bg-surface-1 border-r border-white/5
      transition-transform duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
    `}>
      {/* Logo row */}
      <div className="flex items-center justify-between px-4 h-14 border-b border-white/5">
        <div className="flex items-center gap-2.5">
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
        <button onClick={onClose} className="md:hidden p-1 text-white/30 hover:text-white transition-colors">
          <X size={16} />
        </button>
      </div>

      {/* New chat */}
      <div className="px-3 py-3">
        <button onClick={onNew}
          className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium
            border border-dashed border-white/10 text-white/40 hover:text-white hover:border-white/20
            hover:bg-white/3 transition-all duration-200">
          <Plus size={15} /> New conversation
        </button>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto px-2 pb-4">
        {conversations.length > 0 && (
          <>
            <div className="px-2 py-1.5 text-[10px] font-semibold text-white/20 tracking-widest uppercase font-mono">
              Recent
            </div>
            {conversations.map(conv => (
              <button key={conv.id} onClick={() => onSelect(conv.id)}
                className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm
                  transition-all duration-150 text-left mb-0.5 group
                  ${activeId === conv.id
                    ? 'bg-ascendra-500/12 border border-ascendra-500/20 text-white'
                    : 'text-white/45 hover:text-white/80 hover:bg-white/4'
                  }`}>
                <MessageSquare size={14} className="flex-shrink-0 opacity-60" />
                <span className="truncate text-xs">{conv.title}</span>
              </button>
            ))}
          </>
        )}
      </div>

      {/* Footer */}
      <div className="px-3 py-3 border-t border-white/5">
        <Link href="/"
          className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-white/30
            hover:text-white/60 hover:bg-white/4 transition-all duration-150">
          <Home size={13} /> Back to home
        </Link>
        <div className="px-3 pt-2">
          <div className="text-[10px] text-white/15 font-mono">Ascendra v2.0 · Personal use only</div>
          <div className="text-[10px] text-white/15 mt-0.5">Review all actions before send</div>
        </div>
      </div>
    </aside>
  )
}
