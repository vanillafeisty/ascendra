import type { Metadata } from 'next'
import { Cormorant_Garamond, DM_Sans, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const display = Cormorant_Garamond({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-display',
})
const body = DM_Sans({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-body',
})
const mono = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-mono',
})

export const metadata: Metadata = {
  title: 'Ascendra — Rise Without Limits',
  description: 'Your autonomous AI career intelligence platform. Land your dream job with zero manual effort.',
  icons: { icon: '/favicon.ico' },
  openGraph: {
    title: 'Ascendra',
    description: 'Rise Without Limits — AI-powered career automation',
    siteName: 'Ascendra',
  }
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${display.variable} ${body.variable} ${mono.variable} font-body bg-surface-0 text-white antialiased`}>
        {children}
      </body>
    </html>
  )
}
