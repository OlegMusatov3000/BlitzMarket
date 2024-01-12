from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.schemas import UserRead, UserCreate
from auth.base_config import auth_backend, fastapi_users
from ads.routers import router as router_ads
from auth.routers import router as router_auth
from config import REDIS_HOST, REDIS_PORT
from complaints.routers import router as router_complaints

app = FastAPI(
    title="Blitz Market"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_ads)
app.include_router(router_auth)
app.include_router(router_complaints)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
