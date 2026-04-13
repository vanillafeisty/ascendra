export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  createdAt?: Date
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

export interface UserProfile {
  name: string
  email: string
  phone: string
  location: string
  targetRole: string
  skills: string[]
  summary: string
  linkedinUrl: string
  githubUrl: string
  portfolioUrl: string
}

export const STARTER_PROMPTS = [
  {
    icon: '🤝',
    title: 'Connect with HRs',
    prompt: 'I want to connect with HRs and hiring managers at product companies in Bangalore who are hiring for frontend developer roles. Help me set this up.',
  },
  {
    icon: '📄',
    title: 'Build My Resume',
    prompt: 'I want to build an ATS-optimized resume. Here\'s my background: [describe your experience, skills, and education]. Build me a strong resume for a Software Developer role.',
  },
  {
    icon: '📧',
    title: 'Cold Email HRs',
    prompt: 'Help me find and email HRs at top tech companies about my React developer profile. I want to do targeted outreach to companies like Razorpay, Swiggy, and CRED.',
  },
  {
    icon: '🗺️',
    title: 'Career Roadmap',
    prompt: 'I know HTML, CSS, JavaScript, and React basics. My goal is to become a Senior Frontend Developer at a product company. Tell me exactly what to do next with free course links.',
  },
  {
    icon: '📝',
    title: 'LinkedIn Post',
    prompt: 'Generate an engaging LinkedIn post about my journey learning React. Make it authentic and likely to get good engagement from the tech community.',
  },
  {
    icon: '🎓',
    title: 'Free Certifications',
    prompt: 'What are the must-do free certifications for a Full Stack Developer role? Include valid YouTube links and course links I can access right now.',
  },
]
