from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Tag(BaseModel):
    """
    칭호 모델
    """
    name: str = Field(..., example="개귀여움")
    description: str = Field(..., example="개귀여우면 획득")

class ProfileResp(BaseModel):
    """
    프로필 리스폰스 모델
    """
    user_id: str = Field(..., example="changjjjjjjjj")
    home_nickname: str = Field(..., example="멍멍홈")
    nickname: str = Field(..., example="멍멍이")
    kind: str = Field(..., example="이탈리안 하운드")
    total_walked_dist: Optional[float] = Field(None, example=163.2)
    best_rank: Optional[int] = Field(None, example=1)
    visitors: int = Field(..., example=123456)
    tags: Optional[List[Tag]] = Field(None, example=[
        {"name": "개귀여움", "description": "개귀여우면 획득"},
        {"name": "개빠름", "description": "개빠르면 획득"},
        {"name": "개똑똑함", "description": "개똑똑하면 획득"},
    ])
    description: Optional[str] = Field(None, example="멍멍이는 멍멍 짖습니다.")
    profile_image_url: Optional[HttpUrl] \
        = Field(None, example="https://test.s3.amazonaws.com/test/test.jpg")

class ProfileUpdateReq(BaseModel):
    """
    프로필 업데이트 요청 모델
    """
    home_nickname: str = Field(..., example="멍멍홈")
    nickname: str = Field(..., example="멍멍이")
    hide_walked_dist: bool = Field(..., example=False)
    hide_best_rank: bool = Field(..., example=True)
    tags: Optional[List[Tag]] = Field(None, example=[
        {"name": "개귀여움", "description": "개귀여우면 획득"},
        {"name": "개빠름", "description": "개빠르면 획득"},
        {"name": "개똑똑함", "description": "개똑똑하면 획득"},
    ])
    description: Optional[str] = Field(None, example="멍멍이는 멍멍 짖습니다 2.")
    profile_image_url: Optional[HttpUrl] \
        = Field(None, example="https://test.s3.amazonaws.com/test/test2.jpg")

class ProfileTagUpdateReq(BaseModel):
    """
    프로필 칭호 업데이트 요청 모델
    """
    tags: List[Tag] = Field(..., example=[
        {"name": "개귀여움", "description": "개귀여우면 획득"},
        {"name": "개빠름", "description": "개빠르면 획득"},
        {"name": "개똑똑함", "description": "개똑똑하면 획득"},
    ])

class VisitorProfileResp(BaseModel):
    """
    방문자 프로필 리스폰스 모델
    """
    user_id: str
    nickname: str
    profile_image_url: Optional[HttpUrl]