import traceback

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from ads.models import Ad, AdType, Comment, Review
from ads.schemas import AdCreate, CommentCreate, ReviewCreate
from constants import CRITICAL_ERROR
from config import logger
from database import get_async_session
from telegram_bot import send_message_to_telegram

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
    try:
        ad_values = new_ad.model_dump()
        ad_values["user_id"] = current_user.id
        stmt = insert(Ad).values(**ad_values)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "data": ad_values,
            "details": None
        }
    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.get("/", responses={
    500: {"description": "Internal Server Error"}
})
async def get_list_ads(
    ads_type: AdType,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Ad).where(
            Ad.type == ads_type
        ).order_by(Ad.created_at.desc()).limit(size).offset((page - 1) * size)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.scalars().all(),
            "details": None,
            "page": page,
            "size": size,
        }
    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.get("/{ad_id}", responses={
    500: {"description": "Internal Server Error"}
})
async def get_detail_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        ad = await session.get(Ad, ad_id)

        return {
            "status": "success",
            "data": ad,
            "details": None
        }
    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.put("/{ad_id}/move_ad", responses={
    403: {"description": "You do not have permission to access this resource"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def move_ad(
    ad_id: int,
    ads_type: AdType,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    try:
        if current_user.role_id != 2:
            return JSONResponse(status_code=403, content={
                    "status": "error",
                    "data": None,
                    "details": "You dont have access to this"
                })

        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Ad not found"
                })

        await session.execute(
            update(Ad).where(Ad.id == ad_id).values(type=ads_type)
        )
        await session.commit()

        return {
            "status": "success",
            "data": ad,
            "details": None
        }

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.delete("/{ad_id}", status_code=204, responses={
    403: {"description": "You do not have permission to access this resource"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    try:
        ad_to_delete = await session.get(Ad, ad_id)

        if ad_to_delete is None:
            return JSONResponse(status_code=404, content={
                "status": "error",
                "data": None,
                "details": "Ad not found"
            })

        if ad_to_delete.user_id != current_user.id:
            return JSONResponse(status_code=403, content={
                "status": "error",
                "data": None,
                "details": "You do not have permission to access this resource"
            })

        await session.delete(ad_to_delete)
        await session.commit()

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.post("/{ad_id}/comments", status_code=201, responses={
    401: {"description": "Unauthorized"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def add_comment(
    ad_id: int,
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    try:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Ad not found"
                })

        comment_values = comment_data.model_dump()
        comment_values["user_id"] = current_user.id
        comment_values["ad_id"] = ad_id
        stmt = insert(Comment).values(**comment_values)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": comment_values, "details": None}

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.get("/{ad_id}/comments", responses={
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def get_comments_for_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100),
):
    try:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Ad not found"
                })

        query = select(Comment).where(
            Comment.ad_id == ad_id
        ).order_by(
            Comment.created_at.desc()
        ).limit(size).offset((page - 1) * size)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None,
            "page": page,
            "size": size,
        }

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.delete("/comments/{comment_id}", status_code=204, responses={
    403: {"description": "Access forbidden for this role"},
    404: {"description": "Comment not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        if current_user.role_id != 2:
            return JSONResponse(status_code=403, content={
                    "status": "error",
                    "data": None,
                    "details": "You dont have access to this"
                })

        comment = await session.get(Comment, comment_id)
        if comment is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Comment not found"
                })
        await session.delete(comment)
        await session.commit()

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.post("/{ad_id}/reviews", status_code=201, responses={
    400: {"description": "Invalid review"},
    401: {"description": "Unauthorized"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def add_review(
    ad_id: int,
    review_data: ReviewCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    try:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Ad not found"
                })

        query = select(Review).where(and_(
                Review.ad_id == ad_id,
                Review.user_id == current_user.id
            ))
        existing_complaint = await session.execute(query)
        if existing_complaint.scalars().all():
            return JSONResponse(status_code=400, content={
                "status": "error",
                "data": None,
                "details": "Repeated review"
            })

        if not (1 <= review_data.rating <= 5):
            return JSONResponse(status_code=400, content={
                "status": "error",
                "data": None,
                "details": "Invalid rating. Must be one of: 1, 2, 3, 4, 5"
            })

        review_values = review_data.model_dump()
        review_values["user_id"] = current_user.id
        review_values["ad_id"] = ad_id
        stmt = insert(Review).values(**review_values)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": review_values,
            "details": None
        }

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)


@router.get("/{ad_id}/reviews", responses={
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def get_reviews_for_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100),
):
    try:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    "status": "error",
                    "data": None,
                    "details": "Ad not found"
                })

        query = select(Review).where(
            Review.ad_id == ad_id
        ).order_by(
            Review.created_at.desc()
        ).limit(size).offset((page - 1) * size)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None,
            "page": page,
            "size": size,
        }

    except Exception as error:
        logger.error(f'{error}\n{traceback.format_exc()}')
        send_message_to_telegram(error)
        raise HTTPException(status_code=500, detail=CRITICAL_ERROR)
