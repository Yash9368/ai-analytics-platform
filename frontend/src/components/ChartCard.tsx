/* ============================================
   ChartCard Component
   Reusable wrapper for all chart visualizations.
   Provides consistent styling, title, and loading state.
   ============================================ */

"use client";

import React from "react";

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
  loading?: boolean;
  action?: React.ReactNode;
}

export default function ChartCard({
  title,
  subtitle,
  children,
  className = "",
  loading = false,
  action,
}: ChartCardProps) {
  return (
    <div className={`glass-card p-5 ${className}`}>
      {/* ---- Header ---- */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3
            className="text-sm font-semibold"
            style={{ color: "var(--text-primary)" }}
          >
            {title}
          </h3>
          {subtitle && (
            <p
              className="text-xs mt-0.5"
              style={{ color: "var(--text-muted)" }}
            >
              {subtitle}
            </p>
          )}
        </div>
        {action && <div>{action}</div>}
      </div>

      {/* ---- Chart Content ---- */}
      {loading ? (
        <div className="flex items-center justify-center" style={{ height: "250px" }}>
          <div className="flex flex-col items-center gap-3">
            <div
              className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
              style={{ borderColor: "var(--accent-blue)", borderTopColor: "transparent" }}
            />
            <span className="text-xs" style={{ color: "var(--text-muted)" }}>
              Loading chart data...
            </span>
          </div>
        </div>
      ) : (
        <div>{children}</div>
      )}
    </div>
  );
}
