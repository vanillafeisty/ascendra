import type { Metadata } from 'next'
import { Playfair_Display, DM_Sans, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const display = Playfair_Display({
  subsets: ['latin'],
  weight: ['400','500','600','700'],
  variable: '--font-display',
})
const body = DM_Sans({
  subsets: ['latin'],
  weight: ['300','400','500','600'],
  variable: '--font-body',
})
const mono = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['400','500'],
  variable: '--font-mono',
})

export const metadata: Metadata = {
  title: 'Ascendra — Rise Without Limits',
  description: 'Your autonomous AI career intelligence assistant.',
  icons: { icon: '/favicon.ico' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${body.variable} ${mono.variable} font-body`}>
        {children}
      </body>
    </html>
  )
}
