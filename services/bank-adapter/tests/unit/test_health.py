"""Unit tests for health check endpoint."""

import pytest
from httpx import AsyncClient

from bank_adapter.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint returns healthy status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Bank Adapter Service"
    assert data["version"] == "0.1.0"
    assert "checks" in data
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["cache"] == "ok"