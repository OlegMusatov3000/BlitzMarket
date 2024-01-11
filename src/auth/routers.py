import traceback

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from constants import CRITICAL_ERROR
from config import logger
from database import get_async_session
from telegram_bot import send_message_to_telegram


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.put("/{user_id}/change_role_or_active", status_code=200, responses={
    403: {"description": "Access forbidden for this role"},
    404: {"description": "User not found"},
    500: {"description": "Internal Server Error"}
})
async def change_user_role(
    user_id: int,
    current_user: User = Depends(current_user),
    value_role_id: int = Query(ge=1, le=2, default=1),
    value_active: int = Query(ge=0, le=1, default=1),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        if current_user.role_id != 2:
            return JSONResponse(status_code=403, content={
                    "status": "error",
                    "data": None,
                    "detail": "You dont have access to this"
                })

        user_to_update = await session.get(User, user_id)
        if user_to_update is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "detail": "User not found"
                })

        await session.execute(
            update(User).where(User.id == user_id).values(
                role_id=value_role_id, is_active=value_active
            )
        )
        await session.commit()

        return {
            "status": "success",
            "data": user_to_update,
            "details": None
        }

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)
