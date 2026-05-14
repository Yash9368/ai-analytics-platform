/* ============================================
   Main Page — Dashboard Entry Point
   
   This is the root page of the app.
   It composes Sidebar + Header + Dashboard
   into a full application layout.
   ============================================ */

"use client";

import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import Dashboard from "@/components/Dashboard";

export default function Home() {
  // ---- State ----
  const [activeNav, setActiveNav] = useState("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [dateRange, setDateRange] = useState("28d");
  const [loading, setLoading] = useState(false);

  // ---- Refresh Handler ----
  const handleRefresh = () => {
    setLoading(true);
    // The useAnalytics hook handles the actual fetch
    // We just trigger a re-render by updating dateRange state
    setDateRange((prev) => prev); // Force re-render
    setTimeout(() => setLoading(false), 1200);
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* ---- Sidebar ---- */}
      <Sidebar
        activeItem={activeNav}
        onItemClick={setActiveNav}
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* ---- Main Content Area ---- */}
      <main
        className="flex-1 flex flex-col overflow-hidden transition-all duration-300"
        style={{
          marginLeft: sidebarCollapsed ? "72px" : "var(--sidebar-width)",
        }}
      >
        {/* Header */}
        <Header
          dateRange={dateRange}
          onDateRangeChange={setDateRange}
          onRefresh={handleRefresh}
          loading={loading}
        />

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <Dashboard
            dateRange={dateRange}
            loading={loading}
            setLoading={setLoading}
          />
        </div>
      </main>
    </div>
  );
}
