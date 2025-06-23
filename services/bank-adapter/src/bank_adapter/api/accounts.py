"""Account management endpoints."""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/accounts")


@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="List accounts",
    description="Get all accounts across bank connections",
)
async def list_accounts() -> List[Dict[str, Any]]:
    """List all accounts.
    
    Returns:
        List of accounts
    """
    # TODO: Implement actual account listing
    return []


@router.get(
    "/{account_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get account details",
    description="Get detailed information about a specific account",
)
async def get_account(account_id: str) -> Dict[str, Any]:
    """Get account details.
    
    Args:
        account_id: Account identifier
        
    Returns:
        Account details
    """
    # TODO: Implement account retrieval
    return {
        "id": account_id,
        "name": "Checking Account",
        "type": "checking",
        "balance": 1000.00,
    }