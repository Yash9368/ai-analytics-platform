/* ============================================
   API Service Layer
   Centralized Axios client for backend communication.
   All API calls go through this module.
   ============================================ */

import axios from "axios";
import { API_BASE_URL } from "@/lib/constants";

// ============================================
// Axios Instance with defaults
// ============================================
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15 second timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// ============================================
// Response Interceptor — global error handling
// ============================================
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("[API Error]", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ============================================
// API Endpoints
// ============================================

/**
 * Health check — verify backend is running
 */
export const checkHealth = () => api.get("/health");

/**
 * Get overview analytics data (total users, sessions, etc.)
 * Will be connected in Phase 7 when backend is ready.
 */
export const getAnalyticsOverview = (dateRange: string = "28d") =>
  api.get(`/api/analytics/overview?date_range=${dateRange}`);

/**
 * Get traffic data over time (for line charts)
 */
export const getTrafficData = (dateRange: string = "28d") =>
  api.get(`/api/analytics/traffic?date_range=${dateRange}`);

/**
 * Get device breakdown (for pie charts)
 */
export const getDeviceData = (dateRange: string = "28d") =>
  api.get(`/api/analytics/devices?date_range=${dateRange}`);

/**
 * Get top pages (for bar charts)
 */
export const getTopPages = (dateRange: string = "28d") =>
  api.get(`/api/analytics/top-pages?date_range=${dateRange}`);

/**
 * Get AI-generated insights from Claude MCP
 * Will be connected in Phase 8.
 */
export const getAIInsights = () => api.get("/api/insights");

export default api;
