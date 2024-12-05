# api/routes/context_routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..controllers.context_controller import ContextController
from ..middleware.auth_middleware import verify_api_key
from ..schemas.monitoring_schemas import ContextUpdate

router = APIRouter(prefix="/v1/context", tags=["context"])
controller = ContextController()

@router.get("/{api_name}")
async def get_api_context(
    api_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Get current context for an API."""
    try:
        return await controller.get_api_context(api_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{api_name}")
async def update_api_context(
    api_name: str,
    context_update: ContextUpdate,
    api_key: str = Depends(verify_api_key)
):
    """Update context for an API."""
    try:
        return await controller.update_api_context(
            api_name,
            context_update.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{api_name}/dependencies")
async def get_api_dependencies(
    api_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Get dependency information for an API."""
    try:
        return await controller.get_dependency_info(api_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))