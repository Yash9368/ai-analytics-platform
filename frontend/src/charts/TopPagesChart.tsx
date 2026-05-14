/* ============================================
   TopPagesChart Component
   Horizontal bar chart showing top pages
   by page views with gradient bars.
   ============================================ */

"use client";

import React from "react";
import type { TopPage } from "@/hooks/useAnalytics";

interface TopPagesChartProps {
  data: TopPage[];
}

export default function TopPagesChart({ data }: TopPagesChartProps) {
  // Find max views for relative bar sizing
  const maxViews = Math.max(...data.map((p) => p.views));

  return (
    <div className="space-y-3">
      {/* ---- Table Header ---- */}
      <div
        className="flex items-center gap-4 px-2 pb-2"
        style={{ borderBottom: "1px solid var(--glass-border)" }}
      >
        <span
          className="flex-1 text-[10px] font-semibold uppercase tracking-wider"
          style={{ color: "var(--text-muted)" }}
        >
          Page
        </span>
        <span
          className="w-20 text-right text-[10px] font-semibold uppercase tracking-wider"
          style={{ color: "var(--text-muted)" }}
        >
          Views
        </span>
        <span
          className="w-16 text-right text-[10px] font-semibold uppercase tracking-wider"
          style={{ color: "var(--text-muted)" }}
        >
          Avg Time
        </span>
      </div>

      {/* ---- Page Rows ---- */}
      {data.map((page, index) => {
        const percentage = (page.views / maxViews) * 100;

        return (
          <div
            key={page.page}
            className={`flex items-center gap-4 px-2 py-2 rounded-lg transition-all duration-200 cursor-pointer hover:bg-white/[0.03] animate-fade-in-up stagger-${index + 1}`}
          >
            {/* Page name with progress bar */}
            <div className="flex-1 min-w-0">
              <span
                className="text-sm font-medium block mb-1.5 truncate"
                style={{ color: "var(--text-primary)" }}
              >
                {page.page}
              </span>
              {/* Progress bar */}
              <div
                className="h-1.5 rounded-full overflow-hidden"
                style={{ background: "rgba(255, 255, 255, 0.04)" }}
              >
                <div
                  className="h-full rounded-full transition-all duration-1000 ease-out"
                  style={{
                    width: `${percentage}%`,
                    background:
                      index === 0
                        ? "var(--gradient-primary)"
                        : index === 1
                        ? "var(--gradient-accent)"
                        : "var(--gradient-success)",
                  }}
                />
              </div>
            </div>

            {/* Views count */}
            <span
              className="w-20 text-right text-sm font-semibold tabular-nums"
              style={{ color: "var(--text-primary)" }}
            >
              {page.views.toLocaleString()}
            </span>

            {/* Average time */}
            <span
              className="w-16 text-right text-xs tabular-nums"
              style={{ color: "var(--text-muted)" }}
            >
              {page.avgTime}
            </span>
          </div>
        );
      })}
    </div>
  );
}
