/* ============================================
   App Constants & Configuration
   Centralized values used across the frontend
   ============================================ */

// Backend API base URL — controlled by environment variable
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Navigation items for the sidebar
export const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: "LayoutDashboard" },
  { id: "analytics", label: "Analytics", icon: "BarChart3" },
  { id: "audience", label: "Audience", icon: "Users" },
  { id: "realtime", label: "Real-time", icon: "Activity" },
  { id: "insights", label: "AI Insights", icon: "Sparkles" },
  { id: "reports", label: "Reports", icon: "FileText" },
  { id: "settings", label: "Settings", icon: "Settings" },
] as const;

// Date range presets for the analytics filter
export const DATE_RANGES = [
  { label: "Today", value: "today" },
  { label: "Yesterday", value: "yesterday" },
  { label: "Last 7 Days", value: "7d" },
  { label: "Last 28 Days", value: "28d" },
  { label: "Last 90 Days", value: "90d" },
  { label: "Last 12 Months", value: "12m" },
] as const;

// Chart color palette — consistent across all charts
export const CHART_COLORS = {
  primary: "#4f8cff",
  secondary: "#a855f7",
  accent: "#ec4899",
  success: "#34d399",
  warning: "#fb923c",
  danger: "#f87171",
  cyan: "#22d3ee",
  palette: [
    "#4f8cff",
    "#a855f7",
    "#ec4899",
    "#34d399",
    "#fb923c",
    "#22d3ee",
    "#f87171",
  ],
};
