/* ============================================
   Dashboard Component
   Main dashboard layout that composes all
   sub-components: stats, charts, and AI insights.
   ============================================ */

"use client";

import React from "react";
import {
  Users,
  MousePointerClick,
  Eye,
  Timer,
} from "lucide-react";
import { useAnalytics } from "@/hooks/useAnalytics";
import StatCard from "@/components/StatCard";
import ChartCard from "@/components/ChartCard";
import AIInsightsPanel from "@/components/AIInsightsPanel";
import TrafficChart from "@/charts/TrafficChart";
import DeviceChart from "@/charts/DeviceChart";
import TopPagesChart from "@/charts/TopPagesChart";

interface DashboardProps {
  dateRange: string;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

export default function Dashboard({
  dateRange,
}: DashboardProps) {
  const {
    overview,
    traffic,
    devices,
    topPages,
    insights,
    loading,
  } = useAnalytics(dateRange);

  // Stat cards configuration
  const stats = overview
    ? [
        {
          title: "Total Users",
          value: overview.totalUsers,
          trend: overview.usersTrend,
          icon: <Users size={18} className="text-white" />,
          gradient: "linear-gradient(135deg, #4f8cff, #6366f1)",
        },
        {
          title: "Sessions",
          value: overview.totalSessions,
          trend: overview.sessionsTrend,
          icon: <MousePointerClick size={18} className="text-white" />,
          gradient: "linear-gradient(135deg, #a855f7, #ec4899)",
        },
        {
          title: "Page Views",
          value: overview.pageViews,
          trend: overview.pageViewsTrend,
          icon: <Eye size={18} className="text-white" />,
          gradient: "linear-gradient(135deg, #22d3ee, #34d399)",
        },
        {
          title: "Bounce Rate",
          value: `${overview.bounceRate}%`,
          trend: overview.bounceTrend,
          icon: <Timer size={18} className="text-white" />,
          gradient: "linear-gradient(135deg, #fb923c, #f87171)",
        },
      ]
    : [];

  return (
    <div className="space-y-6">
      {/* ---- Stat Cards Row ---- */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {loading
          ? [0, 1, 2, 3].map((i) => (
              <StatCard
                key={i}
                title=""
                value=""
                trend={0}
                icon={null}
                gradient=""
                index={i}
                loading={true}
              />
            ))
          : stats.map((stat, index) => (
              <StatCard key={stat.title} {...stat} index={index} />
            ))}
      </div>

      {/* ---- Charts Row ---- */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Traffic Chart — takes 2 columns */}
        <ChartCard
          title="Traffic Overview"
          subtitle="Users, sessions, and page views over time"
          className="lg:col-span-2 animate-fade-in-up stagger-2"
          loading={loading}
        >
          <TrafficChart data={traffic} />
        </ChartCard>

        {/* Device Breakdown */}
        <ChartCard
          title="Device Breakdown"
          subtitle="Visitors by device type"
          className="animate-fade-in-up stagger-3"
          loading={loading}
        >
          <div className="flex items-center justify-center py-4">
            <DeviceChart data={devices} />
          </div>
        </ChartCard>
      </div>

      {/* ---- Bottom Row: Top Pages + AI Insights ---- */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Top Pages */}
        <ChartCard
          title="Top Pages"
          subtitle="Most visited pages by views"
          className="animate-fade-in-up stagger-3"
          loading={loading}
        >
          <TopPagesChart data={topPages} />
        </ChartCard>

        {/* AI Insights */}
        <div className="animate-fade-in-up stagger-4">
          <AIInsightsPanel insights={insights} loading={loading} />
        </div>
      </div>

      {/* ---- Footer ---- */}
      <div className="text-center py-4">
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          Data refreshed automatically • Powered by Google Analytics 4 + Claude MCP
        </p>
      </div>
    </div>
  );
}
