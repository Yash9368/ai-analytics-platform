/* ============================================
   TrafficChart Component
   Area chart showing Users, Sessions, Page Views
   over time using Recharts.
   ============================================ */

"use client";

import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type { TrafficDataPoint } from "@/hooks/useAnalytics";

interface TrafficChartProps {
  data: TrafficDataPoint[];
}

// Custom tooltip with glassmorphism styling
const CustomTooltip = ({ active, payload, label }: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}) => {
  if (!active || !payload) return null;

  return (
    <div
      className="rounded-xl px-4 py-3"
      style={{
        background: "rgba(20, 20, 55, 0.95)",
        border: "1px solid rgba(255, 255, 255, 0.1)",
        backdropFilter: "blur(12px)",
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)",
      }}
    >
      <p
        className="text-xs font-semibold mb-2"
        style={{ color: "var(--text-primary)" }}
      >
        {label}
      </p>
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-2 mb-1">
          <div
            className="w-2 h-2 rounded-full"
            style={{ background: entry.color }}
          />
          <span
            className="text-[11px]"
            style={{ color: "var(--text-secondary)" }}
          >
            {entry.name}:
          </span>
          <span
            className="text-[11px] font-semibold"
            style={{ color: "var(--text-primary)" }}
          >
            {entry.value.toLocaleString()}
          </span>
        </div>
      ))}
    </div>
  );
};

export default function TrafficChart({ data }: TrafficChartProps) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
        <defs>
          {/* Gradient fills for the areas */}
          <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#4f8cff" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#4f8cff" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorSessions" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#a855f7" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#a855f7" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorPageViews" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
          </linearGradient>
        </defs>

        <CartesianGrid
          strokeDasharray="3 3"
          stroke="rgba(148, 163, 184, 0.06)"
          vertical={false}
        />
        <XAxis
          dataKey="date"
          tick={{ fill: "#64748b", fontSize: 11 }}
          axisLine={{ stroke: "rgba(148, 163, 184, 0.1)" }}
          tickLine={false}
        />
        <YAxis
          tick={{ fill: "#64748b", fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          tickFormatter={(value: number) =>
            value >= 1000 ? `${(value / 1000).toFixed(0)}K` : `${value}`
          }
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: "11px", color: "#94a3b8" }}
        />

        <Area
          type="monotone"
          dataKey="pageViews"
          name="Page Views"
          stroke="#22d3ee"
          fill="url(#colorPageViews)"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: "#22d3ee", stroke: "#0a0a1a", strokeWidth: 2 }}
        />
        <Area
          type="monotone"
          dataKey="sessions"
          name="Sessions"
          stroke="#a855f7"
          fill="url(#colorSessions)"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: "#a855f7", stroke: "#0a0a1a", strokeWidth: 2 }}
        />
        <Area
          type="monotone"
          dataKey="users"
          name="Users"
          stroke="#4f8cff"
          fill="url(#colorUsers)"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: "#4f8cff", stroke: "#0a0a1a", strokeWidth: 2 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
