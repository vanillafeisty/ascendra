import ChatInterface from '@/components/ChatInterface'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Chat — Ascendra',
  description: 'Your AI career co-pilot. Ask anything.',
}

export default function ChatPage() {
  return <ChatInterface />
}
