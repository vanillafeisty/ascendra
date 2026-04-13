'use client'
import Link from 'next/link'
import { ArrowRight, Zap, Shield, Brain, Users, Mail, FileText, TrendingUp, Star, ChevronRight } from 'lucide-react'

const FEATURES = [
  { icon: Users, title: 'Smart HR Connect', desc: 'Auto-finds and connects with HRs, hiring managers, and mentors who can actually help you.' },
  { icon: Mail, title: 'Cold Email Engine', desc: 'Discovers valid HR emails and sends personalized cold emails directly — no manual work.' },
  { icon: FileText, title: 'ATS-Semantic Engine', desc: 'NLP-powered resume optimization with TF-IDF keyword alignment and semantic scoring.' },
  { icon: Brain, title: 'Career Intelligence', desc: 'Skill gap analysis, roadmaps, and "what to do next" powered by real market data.' },
  { icon: Zap, title: 'LinkedIn Autopilot', desc: 'Posts, messages, profile updates — all automated with anti-bot stealth layer.' },
  { icon: Shield, title: 'Human-in-the-Loop', desc: 'You review every message before it sends. Full control, zero surprises.' },
]

const CAPABILITIES = [
  'Connect with HRs automatically', 'Send cold messages & emails', 'Build ATS-optimized resumes',
  'Generate weekly LinkedIn posts', 'Tailor resume to any JD', 'Find free courses & certs',
  'Discover HR email addresses', 'Roadmap to your dream role',
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-surface-0 noise overflow-hidden">
      {/* Nav */}
      <nav className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-6 md:px-12 h-16
        bg-surface-0/80 backdrop-blur-xl border-b border-white/5">
        <Logo />
        <div className="flex items-center gap-3">
          <Link href="/chat"
            className="flex items-center gap-2 px-5 py-2 rounded-full text-sm font-semibold
              bg-ascendra-500 hover:bg-ascendra-400 text-white transition-all duration-200
              shadow-lg shadow-ascendra-900/50">
            Open Ascendra <ArrowRight size={15} />
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative min-h-screen flex items-center justify-center px-6 pt-16">
        {/* Background glow */}
        <div className="absolute inset-0 bg-grid opacity-100 pointer-events-none" />
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px]
          rounded-full bg-ascendra-500/5 blur-[120px] pointer-events-none" />
        <div className="absolute top-1/2 left-1/4 w-[300px] h-[300px]
          rounded-full bg-blue-600/5 blur-[80px] pointer-events-none" />

        <div className="relative text-center max-w-4xl mx-auto animate-slide-up">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-8
            border border-ascendra-500/30 bg-ascendra-500/10 text-ascendra-300 text-sm font-medium">
            <Star size={12} className="fill-ascendra-400 text-ascendra-400" />
            AI Career Intelligence Platform
          </div>

          {/* Headline */}
          <h1 className="font-display font-bold leading-[0.95] mb-6" style={{fontSize:'clamp(3rem,8vw,6rem)'}}>
            <span className="text-white">Land Your Dream Job.</span>
            <br />
            <span className="text-gold-gradient">Without Lifting a Finger.</span>
          </h1>

          <p className="text-lg md:text-xl text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
            Ascendra is your autonomous AI career co-pilot. It connects with HRs, sends cold messages,
            builds ATS-optimized resumes, and posts on LinkedIn — all from a single chat.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/chat"
              className="group flex items-center gap-3 px-8 py-4 rounded-2xl text-base font-semibold
                bg-ascendra-500 hover:bg-ascendra-400 text-white transition-all duration-300
                shadow-xl shadow-ascendra-900/60 hover:shadow-ascendra-500/30 hover:-translate-y-0.5">
              Start for Free
              <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="#features"
              className="flex items-center gap-2 px-8 py-4 rounded-2xl text-base font-semibold
                border border-white/10 hover:border-white/20 text-white/70 hover:text-white
                transition-all duration-200 backdrop-blur-sm bg-white/3">
              See Features <ChevronRight size={16} />
            </Link>
          </div>

          {/* Capability pills */}
          <div className="flex flex-wrap justify-center gap-2">
            {CAPABILITIES.map(cap => (
              <span key={cap}
                className="px-3 py-1 rounded-full text-xs font-medium
                  bg-white/4 border border-white/8 text-white/50">
                {cap}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="relative py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white mb-4">
              Everything You Need to <span className="text-gold-gradient">Rise</span>
            </h2>
            <p className="text-white/50 text-lg max-w-2xl mx-auto">
              One AI assistant. Complete career automation. Zero manual work.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title}
                className="group relative p-6 rounded-2xl border border-white/6
                  bg-surface-2 hover:bg-surface-3 hover:border-ascendra-500/25
                  transition-all duration-300 hover:-translate-y-1">
                <div className="w-10 h-10 rounded-xl bg-ascendra-500/15 border border-ascendra-500/25
                  flex items-center justify-center mb-4 group-hover:bg-ascendra-500/20 transition-colors">
                  <Icon size={20} className="text-ascendra-400" />
                </div>
                <h3 className="text-white font-semibold text-base mb-2">{title}</h3>
                <p className="text-white/45 text-sm leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="relative p-12 rounded-3xl border border-ascendra-500/20
            bg-gradient-to-b from-surface-3 to-surface-2 overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-ascendra-500/8 to-transparent" />
            <div className="relative">
              <h2 className="font-display text-4xl md:text-5xl font-bold text-white mb-4">
                Ready to <span className="text-gold-gradient">Ascend?</span>
              </h2>
              <p className="text-white/50 mb-8 text-lg">
                Join thousands of professionals who let Ascendra do the heavy lifting.
              </p>
              <Link href="/chat"
                className="inline-flex items-center gap-3 px-10 py-4 rounded-2xl text-base font-semibold
                  bg-ascendra-500 hover:bg-ascendra-400 text-white transition-all duration-300
                  shadow-xl shadow-ascendra-900/50 hover:-translate-y-0.5">
                Launch Ascendra Free <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8 px-6 text-center text-white/25 text-sm">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Logo small />
        </div>
        <p>© 2026 Ascendra. Rise Without Limits. Personal use only.</p>
      </footer>
    </div>
  )
}

function Logo({ small = false }: { small?: boolean }) {
  return (
    <div className={`flex items-center gap-2.5 ${small ? 'scale-75 origin-left' : ''}`}>
      <div className="relative w-8 h-8 flex items-center justify-center">
        <div className="absolute inset-0 rounded-lg bg-ascendra-500/20 border border-ascendra-500/40" />
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 2L16 15H2L9 2Z" fill="none" stroke="#d4891e" strokeWidth="1.5" strokeLinejoin="round"/>
          <path d="M9 2L9 10" stroke="#d4891e" strokeWidth="1.5" strokeLinecap="round"/>
          <circle cx="9" cy="12" r="1.5" fill="#d4891e"/>
        </svg>
      </div>
      <span className="font-display font-semibold text-lg tracking-tight text-white">Ascendra</span>
    </div>
  )
}
