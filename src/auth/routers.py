from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from database import get_async_session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.put("/{user_id}/change-role", status_code=200, responses={
    403: {"description": "Access forbidden for this role"},
    404: {"description": "User not found"},
    500: {"description": "Internal Server Error"}
})
async def change_user_role(
    user_id: int,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        if current_user.role_id != 2:
            return JSONResponse(status_code=403, content={
                    'status': 'error',
                    'data': None,
                    'detail': 'You dont have access to this'
                })

        user_to_update = await session.get(User, user_id)
        if user_to_update is None:
            return JSONResponse(status_code=404, content={
                    'status': 'error',
                    'data': None,
                    'detail': 'User not found'
                })

        await session.execute(
            update(User).where(User.id == user_id).values(role_id=2)
        )
        await session.commit()

        return {
            'status': 'success',
            'data': user_to_update,
            'details': None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': 'An unexpected error occurred'
        })
