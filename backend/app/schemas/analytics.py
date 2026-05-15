"""
Analytics Schemas — Pydantic Response Models

Defines the exact shape of JSON responses returned by the analytics API.
Pydantic enforces type safety and auto-generates OpenAPI documentation.
"""

from pydantic import BaseModel
from typing import Optional


# ============================================
# Overview Metrics
# ============================================
class AnalyticsOverview(BaseModel):
    """Top-level analytics summary metrics."""
    totalUsers: int = 0
    totalSessions: int = 0
    pageViews: int = 0
    bounceRate: float = 0.0
    avgSessionDuration: str = "0s"
    newUsers: int = 0
    usersTrend: float = 0.0       # % change vs previous period
    sessionsTrend: float = 0.0
    pageViewsTrend: float = 0.0
    bounceTrend: float = 0.0


# ============================================
# Traffic Over Time
# ============================================
class TrafficDataPoint(BaseModel):
    """Single data point for the traffic time-series chart."""
    date: str
    users: int = 0
    sessions: int = 0
    pageViews: int = 0


class TrafficResponse(BaseModel):
    """List of traffic data points."""
    data: list[TrafficDataPoint] = []


# ============================================
# Device Breakdown
# ============================================
class DeviceData(BaseModel):
    """Device category with percentage and color."""
    name: str
    value: float = 0.0
    color: str = "#4f8cff"


class DeviceResponse(BaseModel):
    """List of device breakdown entries."""
    data: list[DeviceData] = []


# ============================================
# Top Pages
# ============================================
class TopPageData(BaseModel):
    """Single page entry with views and time metrics."""
    page: str
    views: int = 0
    avgTime: str = "0s"


class TopPagesResponse(BaseModel):
    """List of top pages."""
    data: list[TopPageData] = []


# ============================================
# API Error Response
# ============================================
class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
