"""
Router modules for API endpoints
"""

from app.routers.auth import router as auth_router
from app.routers.journals import router as journals_router
from app.routers.moods import router as moods_router
from app.routers.ai import router as ai_router

__all__ = [
    "auth_router",
    "journals_router",
    "moods_router", 
    "ai_router"
] 