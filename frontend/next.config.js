/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://forge-media-backend.onrender.com',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://forge-media-backend.onrender.com/api/:path*',
      },
    ]
  }
}

module.exports = nextConfig
