from typing import Annotated

from fastapi import Depends, APIRouter

from app.schemas.user import UserResponse
from app.security.security_config import authenticated_user

router = APIRouter()


@router.get("/clerk_jwt/", response_model=UserResponse)
async def clerk_jwt(current_user: Annotated[str, Depends(authenticated_user)]):
    return UserResponse(userId=current_user)


@router.get("/gated_data/", response_model=dict)
async def gated_data(_: Annotated[str, Depends(authenticated_user)]):
    return {"foo": "bar"}
