from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict


def success_response(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None
) -> JSONResponse:
    """
    성공 응답 표준 포맷
    
    Response Format:
    {
        "status": "success",
        "message": "...",  # Optional
        "data": {...}
    }
    """
    content = {
        "status": "success",
        "data": data
    }
    
    if message:
        content["message"] = message
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )


def error_response(
    message: str,
    status_code: int,
    error_code: Optional[str] = None,
    details: Optional[Dict] = None
) -> JSONResponse:
    """
    에러 응답 표준 포맷
    
    Response Format:
    {
        "status": "error",
        "message": "...",
        "error_code": "...",  # Optional
        "details": {...}      # Optional
    }
    """
    content = {
        "status": "error",
        "message": message
    }
    
    if error_code:
        content["error_code"] = error_code
    
    if details:
        content["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )
