from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
from config.default.api_config import get_api_config

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(
    api_key: str = Security(api_key_header)
) -> str:
    """Verify API key middleware."""
    config = get_api_config()
    if api_key != config.api_key:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )
    return api_key