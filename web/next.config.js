/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: []
  },
  images: {
    domains: ['media.licdn.com', 'avatars.githubusercontent.com']
  }
}

module.exports = nextConfig
