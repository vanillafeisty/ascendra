/**
 * Ascendra Content Moderation
 * Blocks unethical, obscene, harmful, or disrespectful content.
 * Provides warm, redirecting refusal messages.
 */

interface ModerationResult {
  blocked: boolean
  category?: string
  response?: string
}

// Keyword patterns for detection (compiled once)
const PATTERNS = {
  sexual: /\b(porn|nsfw|nude|naked|xxx|sex(?:ual|ually|ting)?|onlyfans|erotic|explicit|adult.?content|lewd|horny|masturbat|genitals?|penis|vagina|breast(?:s)?(?!\s+cancer))\b/i,
  hate: /\b(nigger|faggot|chink|spic|kike|tranny|retard|cunt|slut|whore)\b/i,
  harassment: /\b(i(?:'ll| will) (?:kill|hurt|destroy|ruin) (?:you|him|her|them)|go (?:kill|die)|stalk(?:ing)?|doxx(?:ing)?|threaten(?:ing)?|blackmail)\b/i,
  violence: /\b(bomb(?:ing|make|build)|make.{0,20}weapon|how to (?:kill|murder|stab|shoot)|assassinat(?:e|ion))\b/i,
  fraud: /\b(fake (?:job|offer|degree|certificate)|scam (?:hr|recruiter|company)|phishing|impersonat(?:e|ing))\b/i,
  spam: /\b(bulk spam|mass (?:spam|unsolicited)|spam (?:everyone|all))\b/i,
  defamation: /\b(post (?:something )?(?:bad|nasty|negative|mean) about|trash(?:talk|ing)|publicly (?:shame|humiliate)|ruin (?:their )?reputation)\b/i,
}

const REFUSALS: Record<string, string> = {
  sexual: `I'm not able to create sexual or adult content — that's a firm boundary for me. 💛

But I'm absolutely here to help with your career! Want me to:
- **Craft a powerful LinkedIn post** about a recent project?
- **Build your ATS-optimized resume**?
- **Connect you with HRs** at companies you love?

What would you like to tackle first?`,

  hate: `That's not something I'm able to generate — content targeting people based on their identity goes against everything Ascendra stands for.

I'm here to help you build something great. Let's focus on **your** career:
- What role are you targeting?
- Want me to find HRs who are hiring right now?`,

  harassment: `I can't help with content designed to threaten or harass someone. That could cause real harm — and it would seriously damage your professional reputation too.

Let's channel that energy into something that actually moves your career forward. Tell me about your target role and I'll start working on it immediately. 🚀`,

  violence: `That request isn't something I can help with at all.

If you're frustrated with your job search, I completely understand — it's genuinely hard. Let me help: tell me where you want to work and I'll build you a strategy to get there.`,

  fraud: `Creating fake credentials, deceptive job offers, or impersonating companies isn't something I can do — and honestly, it would destroy the career you're trying to build.

What I *can* do is help you build a **genuinely strong profile** that gets you noticed legitimately. Want to start with your resume or LinkedIn?`,

  spam: `Mass unsolicited spam campaigns will get your email/LinkedIn flagged and hurt your reputation with the very people you want to impress.

Ascendra's approach is **targeted, personalized outreach** — which gets 10x better response rates anyway. Want me to find the right HRs for your specific role and craft personalized messages?`,

  defamation: `Posting negative content about colleagues or managers — even if justified — almost always backfires and hurts your own career.

The most powerful thing you can do is build such an impressive profile that it speaks for itself. Let me help with that instead. What's your current situation?`,
}

export function moderateInput(text: string): ModerationResult {
  const lower = text.toLowerCase()

  for (const [category, pattern] of Object.entries(PATTERNS)) {
    if (pattern.test(lower)) {
      return {
        blocked: true,
        category,
        response: REFUSALS[category] ?? REFUSALS.harassment,
      }
    }
  }

  return { blocked: false }
}

export function moderateOutput(text: string): ModerationResult {
  // Secondary check on generated output
  for (const [category, pattern] of Object.entries(PATTERNS)) {
    if (pattern.test(text)) {
      return {
        blocked: true,
        category,
        response: "I noticed the response I was generating went in an inappropriate direction. Let me refocus on what will actually help your career. What's your main goal right now?",
      }
    }
  }
  return { blocked: false }
}
