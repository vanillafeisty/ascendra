'use client'
import { Zap, User, Copy, Check } from 'lucide-react'
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { Message } from '@/lib/types'

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'
  const [copied, setCopied] = useState(false)

  function copyContent() {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3 py-2 animate-fade-in">
        <div className="max-w-[75%] px-4 py-3 rounded-2xl rounded-tr-none
          bg-ascendra-500/15 border border-ascendra-500/20 text-white/90 text-sm leading-relaxed">
          {message.content}
        </div>
        <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-surface-4 border border-white/8
          flex items-center justify-center mt-0.5">
          <User size={14} className="text-white/50" />
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-start gap-3 py-2 group animate-fade-in">
      <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-ascendra-500/15 border border-ascendra-500/30
        flex items-center justify-center mt-0.5">
        <Zap size={14} className="text-ascendra-400" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-xs font-semibold text-ascendra-400/70 mb-1 font-mono tracking-wide">
          ASCENDRA
        </div>
        <div className="prose-ascendra text-sm">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, className, children, ...props }: any) {
                const isInline = !className
                if (isInline) {
                  return <code className={className} {...props}>{children}</code>
                }
                return (
                  <pre>
                    <code className={className} {...props}>{children}</code>
                  </pre>
                )
              },
              a({ href, children }: any) {
                return (
                  <a href={href} target="_blank" rel="noopener noreferrer"
                    className="text-ascendra-300 hover:text-ascendra-200 underline underline-offset-2">
                    {children}
                  </a>
                )
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        <button onClick={copyContent}
          className="mt-2 flex items-center gap-1.5 text-xs text-white/20 hover:text-white/50
            transition-colors opacity-0 group-hover:opacity-100">
          {copied ? <Check size={12} /> : <Copy size={12} />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
    </div>
  )
}
