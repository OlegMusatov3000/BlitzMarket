from fastapi import FastAPI

from auth.schemas import UserRead, UserCreate
from auth.base_config import auth_backend, fastapi_users
from ads.routers import router as router_ads

app = FastAPI(
    title='Blitz Market'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_ads)
