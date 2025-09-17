/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    serverComponentsExternalPackages: []
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080',
    NEXT_PUBLIC_WS_BASE_URL: process.env.NEXT_PUBLIC_WS_BASE_URL || 'ws://localhost:8080'
  }
}

module.exports = nextConfig