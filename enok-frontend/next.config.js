/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:slug*',
        destination: 'http://localhost:8000/:slug*'
      },
      {
        source: '/api',
        destination: 'http://localhost:8000'
      }
    ]
  },
}

module.exports = nextConfig
