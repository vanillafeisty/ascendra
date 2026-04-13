// For local testing, this points to your machine running api.py
// On Android emulator use: http://10.0.2.2:8000
// On iOS simulator use:    http://localhost:8000
// On real device use:      http://YOUR_PC_LOCAL_IP:8000  (e.g. http://192.168.1.5:8000)
export const BACKEND_URL = 'http://localhost:8000'

export const STARTER_PROMPTS = [
  { icon: '🤝', title: 'Connect HRs', prompt: 'Connect me with HRs and hiring managers at product companies in Bangalore hiring for React developer roles.' },
  { icon: '📄', title: 'Build Resume', prompt: "Build me an ATS-semantic optimized resume for a Software Developer role. I'll share my background now." },
  { icon: '📧', title: 'Cold Emails', prompt: 'Help me find and email HRs at Razorpay, Swiggy, and CRED about my React developer profile.' },
  { icon: '🗺️', title: 'Roadmap', prompt: 'I know HTML, CSS, JS and React basics. My goal is Senior Frontend Developer. Tell me what to do next with free course links.' },
  { icon: '📝', title: 'LinkedIn Post', prompt: 'Generate an engaging LinkedIn post about learning React that will get good tech community engagement.' },
  { icon: '🎓', title: 'Free Certs', prompt: 'What are must-do free certifications for a Full Stack Developer? Include valid YouTube links.' },
]
