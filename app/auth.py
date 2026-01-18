"""Demo access token authentication."""

from fastapi import HTTPException, Query, status

from app.config import settings


async def verify_demo_token(token: str | None = Query(None)) -> None:
    """Verify the demo access token.

    If DEMO_ACCESS_TOKEN is not set, protection is disabled.
    Otherwise, the token query parameter must match.
    """
    if not settings.DEMO_ACCESS_TOKEN:
        return  # Protection disabled

    if token != settings.DEMO_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token",
        )
