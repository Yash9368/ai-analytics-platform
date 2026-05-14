import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // ============================================
  // Production Configuration
  // ============================================

  // Output as standalone for Render deployment
  // This bundles everything needed to run the app
  output: "standalone",

  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },

  // Image optimization settings
  images: {
    domains: [],
    unoptimized: false,
  },

  // Disable x-powered-by header for security
  poweredByHeader: false,

  // Enable React strict mode for better development
  reactStrictMode: true,
};

export default nextConfig;
