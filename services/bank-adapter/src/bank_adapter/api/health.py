"""Health check endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/health",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the service is healthy and operational",
)
async def health_check() -> Dict[str, Any]:
    """Perform health check.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "service": "Bank Adapter Service",
        "version": "0.1.0",
        "checks": {
            "database": "ok",  # TODO: Implement actual DB check
            "cache": "ok",     # TODO: Implement actual cache check
            "external_apis": {
                "plaid": "ok",    # TODO: Implement actual Plaid check
                "yodlee": "ok",   # TODO: Implement actual Yodlee check
            },
        },
    }