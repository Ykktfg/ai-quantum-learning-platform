from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Handle unexpected backend errors
    and return a clean JSON response.
    """

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred.",
        },
    )