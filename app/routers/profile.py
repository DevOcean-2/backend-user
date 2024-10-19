"""
유저관리의 프로필 관련 API
"""
from typing import List
from fastapi import APIRouter
from ..schemas.profile import ProfileResp, ProfileTagUpdateReq, ProfileUpdateReq, VisitorProfileResp

router = APIRouter(
    prefix="/profiles",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=ProfileResp)
async def get_profile(user_id: str):
    """
    특정 유저 프로필 정보 조회 API
    :param user_id:
    :return: user profile
    """
    print(user_id)
    return None


@router.put("")
async def update_profile(profile: ProfileUpdateReq, token: str):
    """
    본인 프로필 수정 API
    :param profile: 업데이트 할 profile
    :param token: auth 확인용
    :return:
    """
    print(profile, token)
    return {"message": "Profile updated"}


@router.put("/tags")
async def update_profile_tags(tags: ProfileTagUpdateReq, token: str):
    """
    본인 프로필 태그 수정 API
    :param tags:
    :param token:
    :return:
    """
    print(tags, token)
    return {"message": "Profile Tags updated"}


@router.get("/visitors", response_model=List[VisitorProfileResp])
async def get_visitors(token: str):
    """
    방문자 리스트 API
    :param token:
    :return:
    """
    print(token)
    return None