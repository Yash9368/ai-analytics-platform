/* ============================================
   useAnalytics Custom Hook
   Fetches analytics data and manages loading/error states.
   In Phase 2, returns mock data. Phase 7 will connect to real API.
   ============================================ */

"use client";

import { useState, useEffect, useCallback } from "react";

// ============================================
// Type Definitions
// ============================================
export interface AnalyticsOverview {
  totalUsers: number;
  totalSessions: number;
  pageViews: number;
  bounceRate: number;
  avgSessionDuration: string;
  newUsers: number;
  usersTrend: number;    // percentage change
  sessionsTrend: number;
  pageViewsTrend: number;
  bounceTrend: number;
}

export interface TrafficDataPoint {
  date: string;
  users: number;
  sessions: number;
  pageViews: number;
}

export interface DeviceData {
  name: string;
  value: number;
  color: string;
}

export interface TopPage {
  page: string;
  views: number;
  avgTime: string;
}

export interface AIInsight {
  id: string;
  title: string;
  description: string;
  type: "positive" | "warning" | "info" | "action";
  metric?: string;
  change?: string;
}

// ============================================
// Mock Data (Phase 2 — replaced by API in Phase 7)
// ============================================
const MOCK_OVERVIEW: AnalyticsOverview = {
  totalUsers: 24847,
  totalSessions: 38291,
  pageViews: 127543,
  bounceRate: 32.4,
  avgSessionDuration: "4m 32s",
  newUsers: 8432,
  usersTrend: 12.5,
  sessionsTrend: 8.3,
  pageViewsTrend: 15.7,
  bounceTrend: -2.1,
};

const MOCK_TRAFFIC: TrafficDataPoint[] = [
  { date: "Mon", users: 3200, sessions: 4800, pageViews: 15200 },
  { date: "Tue", users: 3800, sessions: 5200, pageViews: 17800 },
  { date: "Wed", users: 4100, sessions: 5900, pageViews: 19200 },
  { date: "Thu", users: 3600, sessions: 5100, pageViews: 16400 },
  { date: "Fri", users: 4500, sessions: 6300, pageViews: 21000 },
  { date: "Sat", users: 2800, sessions: 3900, pageViews: 12800 },
  { date: "Sun", users: 2400, sessions: 3400, pageViews: 11600 },
];

const MOCK_DEVICES: DeviceData[] = [
  { name: "Desktop", value: 52, color: "#4f8cff" },
  { name: "Mobile", value: 38, color: "#a855f7" },
  { name: "Tablet", value: 10, color: "#22d3ee" },
];

const MOCK_TOP_PAGES: TopPage[] = [
  { page: "/", views: 32450, avgTime: "2m 15s" },
  { page: "/products", views: 18320, avgTime: "3m 42s" },
  { page: "/about", views: 12890, avgTime: "1m 58s" },
  { page: "/blog/ai-trends", views: 9740, avgTime: "5m 11s" },
  { page: "/pricing", views: 8650, avgTime: "4m 03s" },
];

const MOCK_INSIGHTS: AIInsight[] = [
  {
    id: "1",
    title: "Traffic Surge Detected",
    description:
      "Your website traffic increased by 23% compared to last week. The /blog/ai-trends page is driving most of the growth.",
    type: "positive",
    metric: "+23%",
    change: "vs last week",
  },
  {
    id: "2",
    title: "High Bounce Rate on Mobile",
    description:
      "Mobile bounce rate is 48%, significantly higher than desktop (24%). Consider optimizing mobile page load speed.",
    type: "warning",
    metric: "48%",
    change: "mobile bounce rate",
  },
  {
    id: "3",
    title: "Peak Hours Identified",
    description:
      "Your highest traffic occurs between 10 AM - 2 PM (UTC). Schedule content releases during this window for maximum reach.",
    type: "info",
    metric: "10AM-2PM",
    change: "peak window",
  },
  {
    id: "4",
    title: "Recommended Action",
    description:
      "Create more content similar to /blog/ai-trends — it has 3x higher engagement and 2x longer session duration than average.",
    type: "action",
    metric: "3x",
    change: "engagement",
  },
];

// ============================================
// Hook Implementation
// ============================================
export function useAnalytics(dateRange: string = "28d") {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [traffic, setTraffic] = useState<TrafficDataPoint[]>([]);
  const [devices, setDevices] = useState<DeviceData[]>([]);
  const [topPages, setTopPages] = useState<TopPage[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Phase 2: Using mock data
      // Phase 7: Replace with actual API calls
      await new Promise((resolve) => setTimeout(resolve, 800)); // Simulate network delay

      setOverview(MOCK_OVERVIEW);
      setTraffic(MOCK_TRAFFIC);
      setDevices(MOCK_DEVICES);
      setTopPages(MOCK_TOP_PAGES);
      setInsights(MOCK_INSIGHTS);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch analytics data");
    } finally {
      setLoading(false);
    }
  }, [dateRange]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    overview,
    traffic,
    devices,
    topPages,
    insights,
    loading,
    error,
    refetch: fetchData,
  };
}
