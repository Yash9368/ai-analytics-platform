"""
Analytics API Routes

Exposes REST endpoints for fetching GA4 analytics data.
All routes are prefixed with /api/analytics.

Endpoints:
    GET /api/analytics/overview    → Summary metrics
    GET /api/analytics/traffic     → Traffic over time
    GET /api/analytics/devices     → Device breakdown
    GET /api/analytics/top-pages   → Most viewed pages
"""

from fastapi import APIRouter, HTTPException, Query
import logging

from app.services.ga4_service import ga4_service
from app.schemas.analytics import (
    AnalyticsOverview,
    TrafficResponse,
    DeviceResponse,
    TopPagesResponse,
    ErrorResponse,
)

logger = logging.getLogger(__name__)

# ============================================
# Router with /api/analytics prefix
# ============================================
router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
    responses={500: {"model": ErrorResponse}},
)


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    date_range: str = Query(default="28d", description="Date range: today, yesterday, 7d, 28d, 90d, 12m")
):
    """
    Get analytics overview metrics.
    
    Returns total users, sessions, page views, bounce rate,
    average session duration, and new users.
    """
    try:
        if not ga4_service.is_connected():
            raise HTTPException(
                status_code=503,
                detail="GA4 service not connected. Check credentials and property ID."
            )
        
        overview = ga4_service.get_overview(date_range)
        return overview
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/traffic", response_model=TrafficResponse)
async def get_traffic_data(
    date_range: str = Query(default="28d", description="Date range: today, yesterday, 7d, 28d, 90d, 12m")
):
    """
    Get traffic data over time for time-series charts.
    
    Returns daily users, sessions, and page views.
    """
    try:
        if not ga4_service.is_connected():
            raise HTTPException(
                status_code=503,
                detail="GA4 service not connected. Check credentials and property ID."
            )
        
        traffic = ga4_service.get_traffic(date_range)
        return TrafficResponse(data=traffic)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching traffic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/devices", response_model=DeviceResponse)
async def get_device_breakdown(
    date_range: str = Query(default="28d", description="Date range: today, yesterday, 7d, 28d, 90d, 12m")
):
    """
    Get visitor breakdown by device category.
    
    Returns percentage breakdown of desktop, mobile, tablet, etc.
    """
    try:
        if not ga4_service.is_connected():
            raise HTTPException(
                status_code=503,
                detail="GA4 service not connected. Check credentials and property ID."
            )
        
        devices = ga4_service.get_devices(date_range)
        return DeviceResponse(data=devices)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching devices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-pages", response_model=TopPagesResponse)
async def get_top_pages(
    date_range: str = Query(default="28d", description="Date range: today, yesterday, 7d, 28d, 90d, 12m"),
    limit: int = Query(default=10, ge=1, le=50, description="Number of pages to return"),
):
    """
    Get most visited pages sorted by page views.
    
    Returns page path, view count, and average session duration.
    """
    try:
        if not ga4_service.is_connected():
            raise HTTPException(
                status_code=503,
                detail="GA4 service not connected. Check credentials and property ID."
            )
        
        pages = ga4_service.get_top_pages(date_range, limit)
        return TopPagesResponse(data=pages)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching top pages: {e}")
        raise HTTPException(status_code=500, detail=str(e))
