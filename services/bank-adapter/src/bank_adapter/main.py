"""Main application entry point for Bank Adapter Service."""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bank_adapter.api import health, connections, accounts, transactions
from bank_adapter.core.config import settings
from bank_adapter.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Bank Adapter Service...")
    
    # Initialize database connections, cache, etc.
    # await init_db()
    # await init_cache()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Bank Adapter Service...")
    # await close_db()
    # await close_cache()


# Create FastAPI application
app = FastAPI(
    title="Bank Adapter Service",
    description="Service for integrating with banks and payment providers",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(connections.router, prefix="/api/v1", tags=["connections"])
app.include_router(accounts.router, prefix="/api/v1", tags=["accounts"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])


@app.get("/", include_in_schema=False)
async def root() -> dict[str, Any]:
    """Root endpoint."""
    return {
        "service": "Bank Adapter Service",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
    }