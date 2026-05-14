/* ============================================
   Header Component
   Top navigation bar with search, date range
   selector, notification bell, and profile avatar.
   ============================================ */

"use client";

import React from "react";
import { Search, Bell, RefreshCw, Calendar } from "lucide-react";
import { DATE_RANGES } from "@/lib/constants";

interface HeaderProps {
  dateRange: string;
  onDateRangeChange: (range: string) => void;
  onRefresh: () => void;
  loading: boolean;
}

export default function Header({
  dateRange,
  onDateRangeChange,
  onRefresh,
  loading,
}: HeaderProps) {
  return (
    <header
      className="sticky top-0 z-30 flex items-center justify-between px-6 py-4"
      style={{
        height: "var(--header-height)",
        background: "rgba(10, 10, 26, 0.8)",
        backdropFilter: "blur(12px)",
        borderBottom: "1px solid var(--glass-border)",
      }}
    >
      {/* ---- Left: Page Title ---- */}
      <div>
        <h2
          className="text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Dashboard
        </h2>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          Overview of your analytics performance
        </p>
      </div>

      {/* ---- Right: Controls ---- */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div
          className="hidden md:flex items-center gap-2 px-3 py-2 rounded-xl"
          style={{
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px solid var(--glass-border)",
          }}
        >
          <Search size={16} style={{ color: "var(--text-muted)" }} />
          <input
            id="header-search"
            type="text"
            placeholder="Search analytics..."
            className="bg-transparent outline-none text-sm w-40"
            style={{ color: "var(--text-primary)" }}
          />
        </div>

        {/* Date Range Selector */}
        <div
          className="flex items-center gap-2 px-3 py-2 rounded-xl cursor-pointer"
          style={{
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px solid var(--glass-border)",
          }}
        >
          <Calendar size={16} style={{ color: "var(--accent-blue)" }} />
          <select
            id="date-range-selector"
            value={dateRange}
            onChange={(e) => onDateRangeChange(e.target.value)}
            className="bg-transparent outline-none text-sm cursor-pointer"
            style={{ color: "var(--text-primary)" }}
          >
            {DATE_RANGES.map((range) => (
              <option
                key={range.value}
                value={range.value}
                style={{ background: "var(--bg-secondary)", color: "var(--text-primary)" }}
              >
                {range.label}
              </option>
            ))}
          </select>
        </div>

        {/* Refresh Button */}
        <button
          id="refresh-button"
          onClick={onRefresh}
          className="p-2.5 rounded-xl transition-all duration-200 hover:scale-105"
          style={{
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px solid var(--glass-border)",
            color: "var(--text-muted)",
          }}
          disabled={loading}
        >
          <RefreshCw
            size={16}
            className={loading ? "animate-spin" : ""}
          />
        </button>

        {/* Notifications */}
        <button
          id="notifications-button"
          className="p-2.5 rounded-xl relative transition-all duration-200 hover:scale-105"
          style={{
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px solid var(--glass-border)",
            color: "var(--text-muted)",
          }}
        >
          <Bell size={16} />
          <span
            className="absolute -top-1 -right-1 w-4 h-4 rounded-full flex items-center justify-center text-[9px] font-bold text-white"
            style={{ background: "var(--accent-pink)" }}
          >
            3
          </span>
        </button>

        {/* Profile Avatar */}
        <div
          className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold text-white cursor-pointer transition-all duration-200 hover:scale-105"
          style={{ background: "var(--gradient-primary)" }}
        >
          U
        </div>
      </div>
    </header>
  );
}
