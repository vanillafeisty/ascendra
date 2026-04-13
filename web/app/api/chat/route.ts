import { NextRequest, NextResponse } from 'next/server'
import { moderateInput } from '@/lib/moderation'

export const maxDuration = 60

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export async function POST(req: NextRequest) {
  const { messages } = await req.json()

  // Client-side moderation before hitting the backend
  const lastMsg = messages[messages.length - 1]
  if (lastMsg?.role === 'user') {
    const mod = moderateInput(lastMsg.content)
    if (mod.blocked) {
      return NextResponse.json({ message: mod.response })
    }
  }

  // Forward to FastAPI backend (which uses Groq — free)
  try {
    const res = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages }),
      // Timeout after 30s
      signal: AbortSignal.timeout(30000),
    })

    if (!res.ok) {
      const errText = await res.text()
      return NextResponse.json({
        message: `Backend error (${res.status}): ${errText.slice(0, 200)}`
      })
    }

    const data = await res.json()
    return NextResponse.json(data)

  } catch (err: any) {
    // Backend not running
    if (err?.name === 'TimeoutError' || err?.cause?.code === 'ECONNREFUSED') {
      return NextResponse.json({
        message: [
          '⚠️ **Ascendra backend is not running.**',
          '',
          'Start it with:',
          '```bash',
          'cd backend',
          'python api.py',
          '```',
          '',
          'Then refresh this page. The backend runs on `http://localhost:8000`.',
        ].join('\n')
      })
    }
    return NextResponse.json({ message: `Connection error: ${err?.message}` })
  }
}
