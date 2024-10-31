"""
유저관리의 프로필 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Query
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.db import get_db
from ..schemas.login import User
from ..schemas.profile import UserProfileResponse, UserProfileUpdate
from ..services.profile import get_user_profile, update_user_profile, get_users

router = APIRouter(
    prefix="/profiles",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/users", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """
    유저 리스트 API \n
    :return: List[user]
    """
    users = get_users(db)
    return users

@router.get("", response_model=List[UserProfileResponse])
async def get_profiles(db: Session = Depends(get_db)):
    """
    모든 유저 프로필 정보 조회 API \n
    :return: List[user profile]
    """
    users = get_users(db)
    user_ids = [user.id for user in users]
    data = []
    for user_id in user_ids:
        data.append(get_user_profile(db, user_id))
    return data

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    """
    특정 유저 프로필 정보 조회 API \n
    :param user_id: \n
    :return: user profile
    """
    profile = get_user_profile(db, user_id)
    return profile

@router.patch("/{user_id}", response_model=UserProfileResponse)
async def update_profile(user_id: int, profile_update: UserProfileUpdate, db: Session = Depends(get_db)):
    """
    프로필 정보 수정 API \n
    :param 업데이트할 필드의 값: \n
    :return: user profile
    """
    return update_user_profile(db, user_id, profile_update)


# @router.put("")
# async def update_profile(profile: ProfileUpdateReq, token: str):
#     """
#     본인 프로필 수정 API
#     :param profile: 업데이트 할 profile
#     :param token: auth 확인용
#     :return:
#     """
#     print(profile, token)
#     return {"message": "Profile updated"}


# @router.put("/tags")
# async def update_profile_tags(tags: ProfileTagUpdateReq, token: str):
#     """
#     본인 프로필 태그 수정 API
#     :param tags:
#     :param token:
#     :return:
#     """
#     print(tags, token)
#     return {"message": "Profile Tags updated"}


# @router.get("/visitors", response_model=List[VisitorProfileResp])
# async def get_visitors(token: str):
#     """
#     방문자 리스트 API
#     :param token:
#     :return:
#     """
#     print(token)
#     return None