/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)'],
        body:    ['var(--font-body)'],
        mono:    ['var(--font-mono)'],
      },
      colors: {
        // Warm beige base
        cream:  { DEFAULT:'#F7F3EE', 50:'#FDFCFA', 100:'#F7F3EE', 200:'#EDE4D8', 300:'#DDD0C0', 400:'#C8B8A2' },
        // Sage green accent
        sage:   { DEFAULT:'#7D9B76', 50:'#F2F6F1', 100:'#E1EBE0', 200:'#BFCFBD', 300:'#9BB397', 400:'#7D9B76', 500:'#638060', 600:'#4E6549', 700:'#3A4C37' },
        // Warm brown
        umber:  { DEFAULT:'#8B6F5C', 50:'#F9F5F2', 100:'#EEE4DC', 200:'#D9C4B5', 300:'#C2A38D', 400:'#A88068', 500:'#8B6F5C', 600:'#705748', 700:'#574235' },
        // Stone neutrals
        stone:  { 50:'#FAFAF9', 100:'#F5F4F2', 200:'#EAE8E5', 300:'#D6D2CD', 400:'#B8B2AB', 500:'#8C8680', 600:'#6B6560', 700:'#514D49', 800:'#3A3733', 900:'#252320' },
      },
      animation: {
        'fade-in':  'fadeIn 0.25s ease-out',
        'slide-up': 'slideUp 0.35s cubic-bezier(0.16,1,0.3,1)',
        'pulse-dot':'pulseDot 1.5s ease-in-out infinite',
      },
      keyframes: {
        fadeIn:   { from:{ opacity:0 }, to:{ opacity:1 } },
        slideUp:  { from:{ opacity:0, transform:'translateY(10px)' }, to:{ opacity:1, transform:'translateY(0)' } },
        pulseDot: { '0%,100%':{ opacity:0.3, transform:'scale(0.75)' }, '50%':{ opacity:1, transform:'scale(1)' } },
      },
    },
  },
  plugins: [],
}
