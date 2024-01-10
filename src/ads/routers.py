from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import user
from ads.models import Ad, AdType
from ads.schemas import AdCreate
from database import get_async_session

router = APIRouter(
    prefix="/ads",
    tags=["Ads"]
)


@router.post("/")
async def add_ad(
    new_ad: AdCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: user = Depends(current_user)
):
    ad_values = new_ad.model_dump()
    ad_values["user_id"] = current_user.id
    stmt = insert(Ad).values(**ad_values)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


@router.get("/")
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


@router.get("/{ad_id}")
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


@router.delete("/{ad_id}")
async def delete_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session),
    current_user: user = Depends(current_user)
):
    try:
        query = select(Ad).where(
            and_(Ad.id == ad_id, Ad.user_id == current_user.id)
        )
        result = await session.execute(query)
        ad_to_delete = result.scalar()
        if ad_to_delete:
            await session.delete(ad_to_delete)
            await session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': 'Ad successfully deleted'
            }
        else:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': None,
                'details': 'Ad not found'
            })
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'an unexpected error occurred'
        })
