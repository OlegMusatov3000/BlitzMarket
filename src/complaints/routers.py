from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from ads.models import Ad
from complaints.models import Complaint
from complaints.schemas import ComplaintCreate
from database import get_async_session

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


@router.get("/", responses={
    403: {"description": "Access forbidden for this role"},
    500: {"description": "Internal Server Error"}
})
async def get_list_complaints(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100),
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

        query = select(Complaint).order_by(
            Complaint.created_at.desc()
        ).limit(size).offset((page - 1) * size)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.scalars().all(),
            "details": None,
            "page": page,
            "size": size,
        }

    except Exception:
        raise HTTPException(status_code=500, details={
            "status": "error",
            "data": None,
            "details": "An unexpected error occurred"
        })


@router.post("/{ad_id}", status_code=201, responses={
    400: {"description": "Repeated complaint"},
    401: {"description": "Unauthorized"},
    404: {"description": "Ad not found"},
    500: {"description": "Internal Server Error"}
})
async def add_complaint(
    ad_id: int,
    complaint_data: ComplaintCreate,
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

        query = select(Complaint).where(and_(
                Complaint.for_ad == ad_id,
                Complaint.author == current_user.id
            ))
        existing_complaint = await session.execute(query)
        if existing_complaint.scalars().all():
            return JSONResponse(status_code=400, content={
                "status": "error",
                "data": None,
                "details": "Repeated complaint"
            })

        complaint_values = complaint_data.model_dump()
        complaint_values["for_ad"] = ad_id
        complaint_values["author"] = current_user.id
        stmt = insert(Complaint).values(**complaint_values)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": complaint_values, "details": None}
    except Exception:
        raise HTTPException(status_code=500, details={
            "status": "error",
            "data": None,
            "details": "An unexpected error occurred"
        })
