/* ============================================
   Sidebar Component
   Navigation sidebar with glassmorphism effect,
   active state indicators, and smooth hover animations.
   ============================================ */

"use client";

import React from "react";
import {
  LayoutDashboard,
  BarChart3,
  Users,
  Activity,
  Sparkles,
  FileText,
  Settings,
  Zap,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { NAV_ITEMS } from "@/lib/constants";

// Map icon names to Lucide components
const ICON_MAP: Record<string, React.ElementType> = {
  LayoutDashboard,
  BarChart3,
  Users,
  Activity,
  Sparkles,
  FileText,
  Settings,
};

interface SidebarProps {
  activeItem: string;
  onItemClick: (id: string) => void;
  collapsed: boolean;
  onToggle: () => void;
}

export default function Sidebar({
  activeItem,
  onItemClick,
  collapsed,
  onToggle,
}: SidebarProps) {
  return (
    <aside
      className="fixed left-0 top-0 h-full z-40 flex flex-col transition-all duration-300 ease-in-out"
      style={{
        width: collapsed ? "72px" : "var(--sidebar-width)",
        background: "var(--bg-sidebar)",
        borderRight: "1px solid var(--glass-border)",
      }}
    >
      {/* ---- Logo Area ---- */}
      <div
        className="flex items-center gap-3 px-5 py-6"
        style={{ borderBottom: "1px solid var(--glass-border)" }}
      >
        <div
          className="flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center"
          style={{ background: "var(--gradient-primary)" }}
        >
          <Zap size={20} className="text-white" />
        </div>
        {!collapsed && (
          <div className="animate-fade-in">
            <h1
              className="text-sm font-bold tracking-wide"
              style={{ color: "var(--text-primary)" }}
            >
              Analytics<span className="gradient-text">AI</span>
            </h1>
            <p
              className="text-[10px] font-medium"
              style={{ color: "var(--text-muted)" }}
            >
              Intelligence Platform
            </p>
          </div>
        )}
      </div>

      {/* ---- Navigation Items ---- */}
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = ICON_MAP[item.icon] || LayoutDashboard;
          const isActive = activeItem === item.id;

          return (
            <button
              key={item.id}
              id={`nav-${item.id}`}
              onClick={() => onItemClick(item.id)}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group relative"
              style={{
                background: isActive
                  ? "rgba(79, 140, 255, 0.12)"
                  : "transparent",
                color: isActive
                  ? "var(--accent-blue)"
                  : "var(--text-secondary)",
              }}
              title={collapsed ? item.label : undefined}
            >
              {/* Active indicator bar */}
              {isActive && (
                <div
                  className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 rounded-r-full"
                  style={{ background: "var(--accent-blue)" }}
                />
              )}

              <Icon
                size={20}
                className="flex-shrink-0 transition-colors duration-200"
                style={{
                  color: isActive
                    ? "var(--accent-blue)"
                    : "var(--text-muted)",
                }}
              />

              {!collapsed && (
                <span
                  className="text-sm font-medium transition-colors duration-200"
                  style={{
                    color: isActive
                      ? "var(--accent-blue)"
                      : "var(--text-secondary)",
                  }}
                >
                  {item.label}
                </span>
              )}

              {/* AI badge for Insights tab */}
              {item.id === "insights" && !collapsed && (
                <span
                  className="ml-auto text-[9px] font-bold px-2 py-0.5 rounded-full"
                  style={{
                    background: "var(--gradient-accent)",
                    color: "white",
                  }}
                >
                  AI
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* ---- Collapse Toggle ---- */}
      <div className="px-3 py-4" style={{ borderTop: "1px solid var(--glass-border)" }}>
        <button
          id="sidebar-toggle"
          onClick={onToggle}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl transition-all duration-200"
          style={{
            background: "rgba(255, 255, 255, 0.03)",
            color: "var(--text-muted)",
          }}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          {!collapsed && <span className="text-xs">Collapse</span>}
        </button>
      </div>
    </aside>
  );
}
