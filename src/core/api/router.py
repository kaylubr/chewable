from fastapi import APIRouter

from core.api import auth, oauth, photos

api_router = APIRouter()


@api_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(photos.router)
