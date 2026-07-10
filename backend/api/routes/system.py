from fastapi import APIRouter
from config.setting import settings

router = APIRouter(tags=["System"])


@router.get("/health")
async def health():
    """
    Liveness check.
    Used by Render/Railway/Docker.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0",
    }


@router.get("/ready")
async def ready():
    """
    Readiness check.
    Verify required services are configured.
    """

    checks = {
        "groq": bool(settings.GROQ_API_KEY),
        "embedding": settings.EMBEDDING_MODEL,
        "vector_db": settings.CHROMA_DIR,
    }

    return {
        "ready": all(
            [
                checks["groq"],
            ]
        ),
        "checks": checks,
    }
