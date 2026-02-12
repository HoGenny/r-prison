from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.db import AsyncSessionLocal
from app.core.errors import AppError, app_error_handler, unhandled_exception_handler
from app.schemas.common import HealthResponse
from app.services.seed_service import seed_service


app = FastAPI(title="Gachon Food Map API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.on_event("startup")
async def run_catalog_seed() -> None:
    async with AsyncSessionLocal() as db:
        await seed_service.seed_defaults(db)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(ok=True)


app.include_router(api_router)
