interface ModerationResult {
  blocked: boolean
  response?: string
}

const PATTERNS = {
  sexual: /\b(porn|nsfw|nude|naked|xxx|sex(?:ual|ually|ting)?|onlyfans|erotic|explicit|adult.?content|lewd)\b/i,
  hate: /\b(nigger|faggot|chink|spic|kike|tranny|retard)\b/i,
  harassment: /\b(i(?:'ll| will) (?:kill|hurt|destroy|ruin) (?:you|him|her|them)|go (?:kill|die)|stalk(?:ing)?|doxx(?:ing)?)\b/i,
  violence: /\b(bomb(?:ing|make|build)|make.{0,20}weapon|how to (?:kill|murder|stab|shoot))\b/i,
  fraud: /\b(fake (?:job|offer|degree|certificate)|scam (?:hr|recruiter|company)|phishing)\b/i,
  defamation: /\b(post (?:something )?(?:bad|nasty|negative|mean) about|trash(?:talk|ing)|publicly (?:shame|humiliate))\b/i,
}

const REFUSALS: Record<string, string> = {
  sexual: `That's not something I'm able to create. 💛\n\nI'm here to help build your career! Want me to:\n- Craft a powerful LinkedIn post?\n- Build your ATS resume?\n- Connect you with hiring managers?\n\nWhat would you like to tackle?`,
  hate: `I can't generate that kind of content — it goes against Ascendra's values.\n\nLet's focus on your career instead. What role are you targeting?`,
  harassment: `I can't help with content designed to harass or threaten someone.\n\nLet me channel your energy into something that moves your career forward. Tell me your target role!`,
  violence: `That's not something I'm able to assist with.\n\nIf you're frustrated with your job search — I understand, it's tough. Tell me where you want to work and I'll build you a strategy.`,
  fraud: `Creating fake credentials or deceptive content isn't something I can do — and it would hurt the career you're building.\n\nI can help you build a genuinely strong profile instead. Want to start with your resume or LinkedIn?`,
  defamation: `Posting negative content about colleagues usually backfires and hurts your own reputation.\n\nThe most powerful move is building such an impressive profile it speaks for itself. Let me help with that!`,
}

export function moderateContent(text: string): ModerationResult {
  const lower = text.toLowerCase()
  for (const [category, pattern] of Object.entries(PATTERNS)) {
    if (pattern.test(lower)) {
      return { blocked: true, response: REFUSALS[category] ?? REFUSALS.harassment }
    }
  }
  return { blocked: false }
}
