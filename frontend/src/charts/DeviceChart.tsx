/* ============================================
   DeviceChart Component
   Donut chart showing device breakdown
   (Desktop, Mobile, Tablet) with center label.
   ============================================ */

"use client";

import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { DeviceData } from "@/hooks/useAnalytics";

interface DeviceChartProps {
  data: DeviceData[];
}

// Custom tooltip
const CustomTooltip = ({ active, payload }: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; payload: DeviceData }>;
}) => {
  if (!active || !payload || !payload[0]) return null;

  const entry = payload[0];
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
      <div className="flex items-center gap-2">
        <div
          className="w-3 h-3 rounded-full"
          style={{ background: entry.payload.color }}
        />
        <span
          className="text-xs font-semibold"
          style={{ color: "var(--text-primary)" }}
        >
          {entry.name}: {entry.value}%
        </span>
      </div>
    </div>
  );
};

export default function DeviceChart({ data }: DeviceChartProps) {
  return (
    <div className="flex items-center gap-6">
      {/* ---- Donut Chart ---- */}
      <div className="relative" style={{ width: "180px", height: "180px" }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
              dataKey="value"
              stroke="none"
              animationBegin={200}
              animationDuration={800}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.color}
                  style={{
                    filter: `drop-shadow(0 0 8px ${entry.color}40)`,
                  }}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="text-lg font-bold"
            style={{ color: "var(--text-primary)" }}
          >
            {data.reduce((sum, d) => sum + d.value, 0)}%
          </span>
          <span
            className="text-[10px]"
            style={{ color: "var(--text-muted)" }}
          >
            Total
          </span>
        </div>
      </div>

      {/* ---- Legend ---- */}
      <div className="flex flex-col gap-3">
        {data.map((device) => (
          <div key={device.name} className="flex items-center gap-3">
            <div
              className="w-3 h-3 rounded-full"
              style={{
                background: device.color,
                boxShadow: `0 0 8px ${device.color}50`,
              }}
            />
            <div>
              <span
                className="text-sm font-medium block"
                style={{ color: "var(--text-primary)" }}
              >
                {device.name}
              </span>
              <span
                className="text-xs"
                style={{ color: "var(--text-muted)" }}
              >
                {device.value}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
