# api/middleware/error_handler.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union, Dict
import traceback
from datetime import datetime


class ErrorHandler:
    """Global error handling middleware."""

    async def __call__(
            self,
            request: Request,
            call_next
    ) -> Union[JSONResponse, Dict]:
        try:
            return await call_next(request)

        except Exception as e:
            error_detail = self._get_error_detail(e)
            status_code = self._get_status_code(e)

            return JSONResponse(
                status_code=status_code,
                content=self._format_error_response(request, error_detail)
            )

    def _get_error_detail(self, error: Exception) -> str:
        """Get detailed error message."""
        if hasattr(error, 'detail'):
            return str(error.detail)
        return str(error)

    def _get_status_code(self, error: Exception) -> int:
        """Determine appropriate status code."""
        if hasattr(error, 'status_code'):
            return error.status_code
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    def _format_error_response(
            self,
            request: Request,
            error_detail: str
    ) -> Dict:
        """Format error response."""
        return {
            'timestamp': datetime.now().isoformat(),
            'path': request.url.path,
            'method': request.method,
            'error': error_detail,
            'trace_id': request.state.trace_id if hasattr(request.state, 'trace_id') else None
        }