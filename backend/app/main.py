"""
AI Analytics Platform — FastAPI Application Entry Point

This is the main entry point for the FastAPI backend server.
It initializes the application, configures CORS middleware,
and registers all API route handlers.

Architecture:
    main.py → routes/ → services/ → Google Analytics Data API
                                   → Claude MCP Server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================
# Initialize FastAPI Application
# ============================================
app = FastAPI(
    title="AI Analytics Platform API",
    description="Production-grade API for Google Analytics 4 data with AI-powered insights",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI at /docs
    redoc_url="/redoc",      # ReDoc at /redoc
)

# ============================================
# CORS Middleware Configuration
# ============================================
# Allows the Next.js frontend to communicate with this backend.
# In production, replace "*" with your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Will be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Health Check Endpoint
# ============================================
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — confirms the API is running."""
    return {
        "status": "healthy",
        "service": "AI Analytics Platform API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "api": True,
        "database": False,     # Will be updated when DB is added
        "analytics": False,    # Will be updated in Phase 6
        "mcp": False,          # Will be updated in Phase 8
    }
