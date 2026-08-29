from datetime import datetime, timezone

from fastapi import APIRouter


router = APIRouter()


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health_check():
    """
    Check whether the backend API is running.
    """

    return {
        "success": True,
        "status": "healthy",
        "service": "AI Quantum Learning Platform API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }