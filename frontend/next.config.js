/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://forge-media-backend.onrender.com',
  },
  // Remove rewrites for now to simplify
}

module.exports = nextConfig
