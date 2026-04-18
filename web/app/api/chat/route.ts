import { NextRequest, NextResponse } from 'next/server'

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

// Basic moderation
const BAD = [/\b(porn|nsfw|nude|xxx|sexual|onlyfans|erotic|lewd)\b/i,
             /\b(nigger|faggot|chink|spic|kike)\b/i,
             /\b(i will (?:kill|hurt) you|stalking|doxxing)\b/i,
             /\b(fake (?:job|degree)|scam hr|phishing)\b/i]

export async function POST(req: NextRequest) {
  const { messages } = await req.json()
  const last = messages[messages.length - 1]
  if (last?.role === 'user') {
    const t = last.content.toLowerCase()
    if (BAD.some(p => p.test(t))) {
      return NextResponse.json({ message: "I'm not able to help with that. Let's focus on your career — what role are you targeting? 💛" })
    }
  }
  try {
    const res = await fetch(`${BACKEND}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages }),
      signal: AbortSignal.timeout(30000),
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (err: any) {
    if (err?.cause?.code === 'ECONNREFUSED' || err?.name === 'TimeoutError') {
      return NextResponse.json({ message: '⚠️ **Backend not running.**\n\nStart it:\n```bash\ncd backend\npython api.py\n```\nThen refresh.' })
    }
    return NextResponse.json({ message: `Error: ${err?.message}` })
  }
}
