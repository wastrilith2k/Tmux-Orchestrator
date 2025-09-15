/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    serverComponentsExternalPackages: []
  },
  env: {
    API_BASE_URL: process.env.API_GATEWAY_URL || 'http://localhost:8080',
    WS_BASE_URL: process.env.WS_GATEWAY_URL || 'ws://localhost:8080'
  }
}

module.exports = nextConfig