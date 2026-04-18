'use client'
import Link from 'next/link'
import { ArrowRight, Zap, Shield, Brain, Users, Mail, FileText, TrendingUp, BookOpen, Sparkles } from 'lucide-react'

const FEATURES = [
  { icon: Users,    title: 'Smart HR Connect',     desc: 'Automatically finds and connects you with HRs and hiring managers who are actively hiring.' },
  { icon: Mail,     title: 'Cold Email Engine',     desc: 'Drafts and sends personalized cold emails to the right people at the right companies.' },
  { icon: FileText, title: 'ATS-Semantic Resume',   desc: 'NLP-powered resume that aligns to any job description. Scores 85+ on every ATS.' },
  { icon: Brain,    title: 'Career Intelligence',   desc: 'Skill gap analysis, phased roadmaps, and a clear "what to do next" action plan.' },
  { icon: Zap,      title: 'LinkedIn Autopilot',    desc: 'Posts, messages, and profile updates — automated with human-like behavior.' },
  { icon: Shield,   title: 'Human-in-the-Loop',     desc: 'You review every action before it executes. Full control, zero surprises.' },
]

export default function Home() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--cream)' }}>

      {/* Nav */}
      <nav style={{ borderBottom: '1px solid var(--border)' }}
        className="sticky top-0 z-50 bg-cream-50/90 backdrop-blur-md">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <Logo />
          <div className="flex items-center gap-3">
            <Link href="/chat"
              style={{ background: 'var(--sage)', color: 'var(--cream)' }}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold
                hover:opacity-90 transition-opacity shadow-sm">
              Open Ascendra <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-8 text-sm font-medium"
          style={{ background: 'var(--sage-light)', color: 'var(--sage-600, #4E6549)',
                   border: '1px solid var(--border-sage)' }}>
          <Sparkles size={13} />
          AI Career Intelligence · Groq-powered · Free
        </div>

        <h1 className="font-display font-bold leading-tight mb-6 text-stone-900"
          style={{ fontSize: 'clamp(2.6rem,6vw,4.5rem)', letterSpacing: '-0.02em' }}>
          Land Your Dream Job.<br />
          <span style={{ color: 'var(--sage)' }}>Without Lifting a Finger.</span>
        </h1>

        <p className="text-lg leading-relaxed mb-10 max-w-2xl mx-auto"
          style={{ color: 'var(--stone-500)' }}>
          Ascendra is your autonomous AI career co-pilot. It connects with HRs, sends cold messages,
          builds ATS-optimized resumes, and posts on LinkedIn — all from a single conversation.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link href="/chat"
            style={{ background: 'var(--sage)', color: 'var(--cream)' }}
            className="group flex items-center gap-2 px-8 py-3.5 rounded-2xl text-base font-semibold
              hover:opacity-90 transition-all shadow-md">
            Start for Free
            <ArrowRight size={16} className="group-hover:translate-x-0.5 transition-transform" />
          </Link>
          <a href="#features"
            style={{ color: 'var(--stone-500)', border: '1px solid var(--border)' }}
            className="flex items-center gap-2 px-8 py-3.5 rounded-2xl text-base font-medium
              hover:border-stone-300 hover:text-stone-700 transition-all bg-cream-50">
            See features
          </a>
        </div>
      </section>

      {/* Status bar */}
      <div className="max-w-4xl mx-auto px-6 mb-16">
        <div className="rounded-2xl p-5 flex flex-wrap gap-6 items-center justify-center"
          style={{ background: 'var(--stone-100)', border: '1px solid var(--border)' }}>
          {[
            ['🤝','Connect HRs automatically'],
            ['📧','Send cold emails directly'],
            ['📄','ATS-optimized resumes'],
            ['📝','LinkedIn posts on autopilot'],
            ['🗺️','Career roadmaps'],
            ['🎓','Free course finder'],
          ].map(([icon, label]) => (
            <div key={label} className="flex items-center gap-2 text-sm"
              style={{ color: 'var(--stone-600, #514D49)' }}>
              <span>{icon}</span><span>{label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <section id="features" className="max-w-5xl mx-auto px-6 pb-20">
        <div className="text-center mb-12">
          <h2 className="font-display text-3xl md:text-4xl font-bold mb-3"
            style={{ color: 'var(--stone-900)' }}>
            Everything you need to <span style={{ color: 'var(--sage)' }}>rise</span>
          </h2>
          <p style={{ color: 'var(--stone-500)' }}>One AI. Complete career automation.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card-hover rounded-2xl p-6"
              style={{ background: '#fff', border: '1px solid var(--border)',
                       boxShadow: 'var(--shadow-sm)' }}>
              <div className="w-10 h-10 rounded-xl flex items-center justify-center mb-4"
                style={{ background: 'var(--sage-light)', border: '1px solid var(--border-sage)' }}>
                <Icon size={19} style={{ color: 'var(--sage)' }} />
              </div>
              <h3 className="font-semibold text-sm mb-2" style={{ color: 'var(--stone-900)' }}>{title}</h3>
              <p className="text-sm leading-relaxed" style={{ color: 'var(--stone-500)' }}>{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-3xl mx-auto px-6 pb-24">
        <div className="rounded-3xl p-12 text-center"
          style={{ background: 'var(--sage-light)', border: '1px solid var(--border-sage)' }}>
          <h2 className="font-display text-3xl md:text-4xl font-bold mb-3"
            style={{ color: 'var(--stone-900)' }}>
            Ready to Ascend?
          </h2>
          <p className="mb-8" style={{ color: 'var(--stone-600, #514D49)' }}>
            Your dream job is one conversation away.
          </p>
          <Link href="/chat"
            style={{ background: 'var(--sage)', color: 'var(--cream)' }}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl text-base font-semibold
              hover:opacity-90 transition-opacity shadow-md">
            Launch Ascendra <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--border)', color: 'var(--stone-400, #B8B2AB)' }}
        className="py-8 px-6 text-center text-sm">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Logo small />
        </div>
        <p>© 2026 Ascendra · Rise Without Limits · Personal use only</p>
      </footer>
    </div>
  )
}

export function Logo({ small = false }: { small?: boolean }) {
  return (
    <div className={`flex items-center gap-2 ${small ? 'opacity-60' : ''}`}>
      <div className="w-7 h-7 rounded-lg flex items-center justify-center"
        style={{ background: 'var(--sage-light)', border: '1px solid var(--border-sage)' }}>
        <TrendingUp size={14} style={{ color: 'var(--sage)' }} />
      </div>
      <span className="font-display font-semibold text-base tracking-tight"
        style={{ color: 'var(--stone-900)' }}>
        Ascendra
      </span>
    </div>
  )
}
