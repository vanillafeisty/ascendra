'use client'
import { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { AvatarIcon } from './ChatInterface'
import type { Message } from '@/lib/types'

export default function MessageBubble({ message }: { message: Message }) {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'

  async function copy() {
    await navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  if (isUser) {
    return (
      <div className="flex justify-end py-2 animate-fade-in">
        <div className="max-w-[78%] px-4 py-3 rounded-2xl rounded-tr-sm text-sm leading-relaxed"
          style={{ background:'var(--sage-light)', border:'1px solid var(--border-sage)',
                   color:'var(--stone-800, #3A3733)' }}>
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-start gap-3 py-2 group animate-fade-in">
      <AvatarIcon />
      <div className="flex-1 min-w-0">
        <p className="text-xs font-semibold mb-1.5 tracking-widest uppercase"
          style={{ color:'var(--stone-400,#B8B2AB)', fontFamily:'var(--font-mono)' }}>
          Ascendra
        </p>
        <div className="prose-warm">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, className, children, ...props }: any) {
                return className
                  ? <pre><code className={className} {...props}>{children}</code></pre>
                  : <code className={className} {...props}>{children}</code>
              },
              a({ href, children }: any) {
                return <a href={href} target="_blank" rel="noopener noreferrer">{children}</a>
              }
            }}>
            {message.content}
          </ReactMarkdown>
        </div>
        <button onClick={copy}
          className="mt-1.5 flex items-center gap-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity"
          style={{ color:'var(--stone-400,#B8B2AB)' }}>
          {copied ? <><Check size={11} /> Copied</> : <><Copy size={11} /> Copy</>}
        </button>
      </div>
    </div>
  )
}
