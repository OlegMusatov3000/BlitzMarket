import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import user
from ads.models import ad, AdType
from ads.schemas import AdReadCreate
from database import get_async_session

router = APIRouter(
    prefix="/ads",
    tags=["Ads"]
)


@router.get("/")
async def get_ads(
    ads_type: AdType, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(ad).where(ad.c.type == ads_type)
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


@router.post("/")
async def add_ad(
    new_ad: AdReadCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: user = Depends(current_user)
):
    new_ad.user_id = current_user.id
    stmt = insert(ad).values(**new_ad.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
