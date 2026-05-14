/* ============================================
   StatCard Component
   Animated stat card with gradient icon backgrounds,
   trend indicators, sparkline preview, and hover effects.
   ============================================ */

"use client";

import React from "react";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  trend: number;
  icon: React.ReactNode;
  gradient: string;
  index: number;
  loading?: boolean;
}

export default function StatCard({
  title,
  value,
  trend,
  icon,
  gradient,
  index,
  loading = false,
}: StatCardProps) {
  // Determine trend direction and color
  const isPositive = trend > 0;
  const isNeutral = trend === 0;
  const trendColor = isPositive
    ? "var(--accent-green)"
    : isNeutral
    ? "var(--text-muted)"
    : "var(--accent-red)";

  // Format the value for display
  const formatValue = (val: string | number): string => {
    if (typeof val === "number") {
      if (val >= 1000000) return `${(val / 1000000).toFixed(1)}M`;
      if (val >= 1000) return `${(val / 1000).toFixed(1)}K`;
      return val.toLocaleString();
    }
    return val;
  };

  if (loading) {
    return (
      <div
        className={`glass-card p-5 animate-fade-in-up stagger-${index + 1}`}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="skeleton w-24 h-4" />
          <div className="skeleton w-10 h-10 rounded-xl" />
        </div>
        <div className="skeleton w-32 h-8 mb-2" />
        <div className="skeleton w-20 h-4" />
      </div>
    );
  }

  return (
    <div
      className={`glass-card p-5 cursor-pointer group animate-fade-in-up stagger-${index + 1}`}
    >
      {/* ---- Top Row: Title + Icon ---- */}
      <div className="flex items-center justify-between mb-4">
        <span
          className="text-xs font-semibold uppercase tracking-wider"
          style={{ color: "var(--text-muted)" }}
        >
          {title}
        </span>
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3"
          style={{
            background: gradient,
            boxShadow: `0 4px 15px ${gradient.includes("blue") ? "rgba(79,140,255,0.3)" : "rgba(168,85,247,0.3)"}`,
          }}
        >
          {icon}
        </div>
      </div>

      {/* ---- Value ---- */}
      <div
        className="text-2xl font-extrabold mb-1 transition-transform duration-300"
        style={{ color: "var(--text-primary)" }}
      >
        {formatValue(value)}
      </div>

      {/* ---- Trend Indicator ---- */}
      <div className="flex items-center gap-1.5">
        <div
          className="flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-semibold"
          style={{
            background: `${trendColor}15`,
            color: trendColor,
          }}
        >
          {isPositive ? (
            <TrendingUp size={12} />
          ) : isNeutral ? (
            <Minus size={12} />
          ) : (
            <TrendingDown size={12} />
          )}
          <span>{Math.abs(trend)}%</span>
        </div>
        <span
          className="text-[11px]"
          style={{ color: "var(--text-muted)" }}
        >
          vs last period
        </span>
      </div>

      {/* ---- Mini Sparkline (decorative) ---- */}
      <div className="mt-3 flex items-end gap-[3px] h-8">
        {[40, 65, 45, 80, 55, 90, 70, 85, 60, 95, 75, 88].map(
          (height, i) => (
            <div
              key={i}
              className="flex-1 rounded-t transition-all duration-500 group-hover:opacity-100"
              style={{
                height: `${height}%`,
                background: gradient,
                opacity: 0.3 + (i / 12) * 0.5,
              }}
            />
          )
        )}
      </div>
    </div>
  );
}
