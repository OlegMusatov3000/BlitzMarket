from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from ads.models import Ad, AdType, Comment
from ads.schemas import AdCreate, CommentCreate
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
    try:
        ad_values = new_ad.model_dump()
        ad_values["user_id"] = current_user.id
        stmt = insert(Ad).values(**ad_values)
        await session.execute(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': 'An unexpected error occurred'
        })


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
            'detail': 'An unexpected error occurred'
        })


@router.get("/{ad_id}", responses={
    500: {"description": "Internal Server Error"}
})
async def get_detail_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        ad = await session.get(Ad, ad_id)

        return {
            'status': 'success',
            'data': ad,
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': 'An unexpected error occurred'
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
        ad_to_delete = await session.get(Ad, ad_id)

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
    ad = await session.get(Ad, ad_id)
    if ad is None:
        return JSONResponse(status_code=404, content={
                'status': 'error',
                'data': None,
                'detail': 'Ad not found'
            })

    comment_values = comment_data.model_dump()
    comment_values["user_id"] = current_user.id
    comment_values["ad_id"] = ad_id
    stmt = insert(Comment).values(**comment_values)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", "data": comment_values, "details": None}


@router.get("/{ad_id}/comments", responses={
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def get_comments_for_ad(
    ad_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            return JSONResponse(status_code=404, content={
                    'status': 'error',
                    'data': None,
                    'detail': 'Ad not found'
                })

        comments = await session.get(Comment, ad_id)
        return {
            'status': 'success',
            'data': comments,
            'details': None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'An unexpected error occurred'
        })


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
                    'status': 'error',
                    'data': None,
                    'detail': 'You dont have access to this'
                })

        comment = await session.get(Comment, comment_id)
        if comment is None:
            return JSONResponse(status_code=404, content={
                    'status': 'error',
                    'data': None,
                    'detail': 'Comment not found'
                })
        await session.delete(comment)
        await session.commit()

    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'An unexpected error occurred'
        })
