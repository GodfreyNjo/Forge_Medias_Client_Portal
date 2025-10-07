/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: '.next',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || '',
  }
}

module.exports = nextConfig
