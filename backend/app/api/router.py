from fastapi import APIRouter

from app.api.v1.achievements import router as achievements_router
from app.api.v1.auth import router as auth_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.gacha import router as gacha_router
from app.api.v1.incubations import router as incubations_router
from app.api.v1.items import router as items_router
from app.api.v1.slimes import router as slimes_router
from app.api.v1.todos import router as todos_router
from app.api.v1.users import router as users_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(todos_router)
api_router.include_router(calendar_router)
api_router.include_router(slimes_router)
api_router.include_router(incubations_router)
api_router.include_router(gacha_router)
api_router.include_router(items_router)
api_router.include_router(achievements_router)
