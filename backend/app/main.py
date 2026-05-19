"""
AI Analytics Platform — FastAPI Application Entry Point

This is the main entry point for the FastAPI backend server.
It initializes the application, configures CORS middleware,
registers all API route handlers, and sets up logging.

Architecture:
    main.py → routes/ → services/ → Google Analytics Data API
                                   → Claude MCP Server (Phase 8)
"""

import os
from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================
# Render OAuth Credential Recreation
# (MUST HAPPEN BEFORE IMPORTING ROUTES)
# ============================================
credentials_dir = Path(__file__).parent.parent / "credentials"
credentials_dir.mkdir(exist_ok=True)

client_secret_env = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
token_env = os.getenv("GOOGLE_TOKEN_JSON")

if client_secret_env:
    with open(credentials_dir / "client_secret.json", "w") as f:
        f.write(client_secret_env)

if token_env:
    with open(credentials_dir / "token.json", "w") as f:
        f.write(token_env)

from app.config.settings import settings
from app.routes import analytics, health, leads

# ============================================
# Logging Configuration
# ============================================
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Register Route Handlers
# ============================================
app.include_router(health.router)         # / and /health
app.include_router(analytics.router)      # /api/analytics/*
app.include_router(leads.router)          # /api/leads/*

# ============================================
# Startup Event
# ============================================
@app.on_event("startup")
async def startup_event():
    """Log configuration on startup."""
    logger.info("=" * 50)
    logger.info(f"🚀 {settings.APP_NAME} v1.0.0")
    logger.info(f"   Environment: {settings.APP_ENV}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   Frontend URL: {settings.FRONTEND_URL}")
    logger.info(f"   GA4 Property ID: {settings.GA4_PROPERTY_ID or '⚠️  NOT SET'}")
    logger.info("=" * 50)
