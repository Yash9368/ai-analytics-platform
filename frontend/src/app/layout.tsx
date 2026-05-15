import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Script from "next/script";
import "./globals.css";

/* ============================================
   GA4 Configuration
   Measurement ID from Google Analytics 4
   ============================================ */
const GA_MEASUREMENT_ID = "G-YLV9FNB9Q2";

/* ============================================
   Font Configuration
   Inter — Modern, clean, highly readable UI font
   ============================================ */
const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
  weight: ["300", "400", "500", "600", "700", "800"],
});

/* ============================================
   SEO Metadata
   ============================================ */
export const metadata: Metadata = {
  title: "AI Analytics Platform — Intelligent Dashboard",
  description:
    "AI-powered analytics dashboard with Google Analytics 4 integration, real-time insights, and Claude MCP intelligence.",
  keywords: [
    "analytics",
    "AI",
    "dashboard",
    "Google Analytics",
    "MCP",
    "Claude",
  ],
  authors: [{ name: "AI Analytics Platform" }],
};

/* ============================================
   Root Layout
   Wraps all pages with fonts, GA4 tracking,
   and background effects.
   ============================================ */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <head>
        {/* ---- Google Analytics 4 (GA4) ---- */}
        {/* Loads the gtag.js library asynchronously */}
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
          strategy="afterInteractive"
        />
        {/* Initializes GA4 with your Measurement ID */}
        <Script id="ga4-init" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_MEASUREMENT_ID}', {
              page_title: document.title,
              send_page_view: true
            });
          `}
        </Script>
      </head>
      <body className="min-h-full flex flex-col">
        {/* Ambient background glow effects */}
        <div className="ambient-glow ambient-glow-1" aria-hidden="true" />
        <div className="ambient-glow ambient-glow-2" aria-hidden="true" />
        <div className="ambient-glow ambient-glow-3" aria-hidden="true" />

        {/* Page content */}
        {children}
      </body>
    </html>
  );
}
