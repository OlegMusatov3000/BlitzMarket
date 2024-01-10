from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from auth.base_config import current_user
from auth.models import User
from ads.models import Ad, AdType
from ads.schemas import AdCreate
from database import get_async_session

router = APIRouter(
    prefix="/ads",
    tags=["Ads"]
)


@router.post("/", status_code=201, responses={
    401: {"description": "Unauthorized"},
    500: {"description": "Internal Server Error"}
})
async def add_ad(
    new_ad: AdCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    ad_values = new_ad.model_dump()
    ad_values["user_id"] = current_user.id
    stmt = insert(Ad).values(**ad_values)
    await session.execute(stmt)
    await session.commit()
    return {
            'status': 'success',
            'data': ad_values,
            'details': None
        }


@router.get("/", responses={
    500: {"description": "Internal Server Error"}
})
async def get_list_ads(
    ads_type: AdType, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Ad).where(Ad.type == ads_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.get("/{ad_id}", responses={
    500: {"description": "Internal Server Error"}
})
async def get_detail_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Ad).where(Ad.id == ad_id)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.delete("/{ad_id}", status_code=204, responses={
    401: {"description": "Unauthorized"},
    403: {"description": "You do not have permission to access this resource"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    try:
        query = select(Ad).where(Ad.id == ad_id)
        result = await session.execute(query)
        ad_to_delete = result.scalar()

        if ad_to_delete is None:
            return JSONResponse(status_code=404, content={
                'status': 'error',
                'data': None,
                'detail': 'Ad not found'
            })

        if ad_to_delete.user_id != current_user.id:
            return JSONResponse(status_code=403, content={
                'status': 'error',
                'data': None,
                'detail': 'You do not have permission to access this resource'
            })

        await session.delete(ad_to_delete)
        await session.commit()

    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': 'An unexpected error occurred'
        })
