/* ============================================
   AI Insights Panel Component
   Displays AI-generated analytics insights
   with type-based styling (positive, warning, info, action).
   Will be powered by Claude MCP in Phase 8.
   ============================================ */

"use client";

import React from "react";
import {
  TrendingUp,
  AlertTriangle,
  Info,
  Lightbulb,
  Sparkles,
  ArrowRight,
} from "lucide-react";
import type { AIInsight } from "@/hooks/useAnalytics";

interface AIInsightsPanelProps {
  insights: AIInsight[];
  loading?: boolean;
}

// Map insight types to visual config
const INSIGHT_CONFIG = {
  positive: {
    icon: TrendingUp,
    gradient: "linear-gradient(135deg, rgba(52, 211, 153, 0.1), rgba(34, 211, 238, 0.05))",
    border: "rgba(52, 211, 153, 0.2)",
    iconBg: "linear-gradient(135deg, #34d399, #22d3ee)",
    metricColor: "var(--accent-green)",
  },
  warning: {
    icon: AlertTriangle,
    gradient: "linear-gradient(135deg, rgba(251, 146, 60, 0.1), rgba(248, 113, 113, 0.05))",
    border: "rgba(251, 146, 60, 0.2)",
    iconBg: "linear-gradient(135deg, #fb923c, #f87171)",
    metricColor: "var(--accent-orange)",
  },
  info: {
    icon: Info,
    gradient: "linear-gradient(135deg, rgba(79, 140, 255, 0.1), rgba(168, 85, 247, 0.05))",
    border: "rgba(79, 140, 255, 0.2)",
    iconBg: "linear-gradient(135deg, #4f8cff, #a855f7)",
    metricColor: "var(--accent-blue)",
  },
  action: {
    icon: Lightbulb,
    gradient: "linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(236, 72, 153, 0.05))",
    border: "rgba(168, 85, 247, 0.2)",
    iconBg: "linear-gradient(135deg, #a855f7, #ec4899)",
    metricColor: "var(--accent-purple)",
  },
};

export default function AIInsightsPanel({
  insights,
  loading = false,
}: AIInsightsPanelProps) {
  if (loading) {
    return (
      <div className="glass-card p-5">
        <div className="flex items-center gap-2 mb-4">
          <div className="skeleton w-6 h-6 rounded" />
          <div className="skeleton w-32 h-5" />
        </div>
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton w-full h-24 mb-3 rounded-xl" />
        ))}
      </div>
    );
  }

  return (
    <div className="glass-card p-5">
      {/* ---- Header ---- */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: "var(--gradient-accent)" }}
          >
            <Sparkles size={16} className="text-white" />
          </div>
          <div>
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              AI Insights
            </h3>
            <p
              className="text-[10px]"
              style={{ color: "var(--text-muted)" }}
            >
              Powered by Claude MCP
            </p>
          </div>
        </div>
        <span
          className="text-[10px] font-semibold px-2 py-1 rounded-full animate-pulse-glow"
          style={{
            background: "rgba(168, 85, 247, 0.15)",
            color: "var(--accent-purple)",
          }}
        >
          ● Live
        </span>
      </div>

      {/* ---- Insight Cards ---- */}
      <div className="space-y-3">
        {insights.map((insight, index) => {
          const config = INSIGHT_CONFIG[insight.type];
          const Icon = config.icon;

          return (
            <div
              key={insight.id}
              className={`p-4 rounded-xl cursor-pointer transition-all duration-300 hover:scale-[1.02] animate-fade-in-up stagger-${index + 1}`}
              style={{
                background: config.gradient,
                border: `1px solid ${config.border}`,
              }}
            >
              <div className="flex items-start gap-3">
                {/* Icon */}
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                  style={{ background: config.iconBg }}
                >
                  <Icon size={14} className="text-white" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4
                      className="text-sm font-semibold"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {insight.title}
                    </h4>
                    {insight.metric && (
                      <span
                        className="text-xs font-bold px-2 py-0.5 rounded-full"
                        style={{
                          background: `${config.metricColor}20`,
                          color: config.metricColor,
                        }}
                      >
                        {insight.metric}
                      </span>
                    )}
                  </div>
                  <p
                    className="text-xs leading-relaxed"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    {insight.description}
                  </p>
                  {insight.change && (
                    <div className="flex items-center gap-1 mt-2">
                      <ArrowRight
                        size={12}
                        style={{ color: config.metricColor }}
                      />
                      <span
                        className="text-[10px] font-medium"
                        style={{ color: "var(--text-muted)" }}
                      >
                        {insight.change}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
