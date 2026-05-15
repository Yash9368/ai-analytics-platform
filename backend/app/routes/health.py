"""
Health Check Routes

Provides endpoints for monitoring the API and its dependencies.
Used by load balancers, uptime monitors, and deployment checks.
"""

from fastapi import APIRouter
from app.services.ga4_service import ga4_service

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint — confirms the API is running."""
    return {
        "status": "healthy",
        "service": "AI Analytics Platform API",
        "version": "1.0.0",
    }


@router.get("/health")
async def health_check():
    """Detailed health check with dependency status."""
    return {
        "status": "healthy",
        "api": True,
        "analytics": ga4_service.is_connected(),
        "mcp": False,  # Will be updated in Phase 8
        "property_id": bool(ga4_service.property_id),
    }
