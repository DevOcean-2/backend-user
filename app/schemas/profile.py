from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from .onboarding import DogBreed

class UserProfileCreate(BaseModel):
    social_id: str = Field(..., description="Kakao's Unique Social ID")         # user의 카카오 social_id
    dog_name: str = Field(..., example="멍멍이")                                 # 강아지 이름
    dog_gender: int = Field(ge=0, le=1, default=0)                              # 0: 수컷, 1: 암컷
    dog_size: int = Field(ge=0, le=2, default=0)                                # 0: 소형견, 1: 중형견, 2: 대형견
    dog_cuteness: int = Field(ge=1, le=5, default=0)                            # 귀여움 정도
    photo_path: Optional[str] = None                                            # 사진 경로
    birth_day: str = Field(min_length=8, max_length=8, pattern=r"^\d{8}$", description="YYYYMMDD")
    current_weight: int = Field(default=0)                                      # 현재 몸무게
    past_weight: Optional[int] = None                                         # 이전 몸무게

    # Foreign Key
    dog_breed: int          # 품종(DogBreed)의 ID
    health_history: str     # 질병 이력 (리스트로 받아서 ,로 분리)
    vaccinations: str       # 백신 이력 (리스트로 받아서 ,로 분리)

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    user_name: str = Field(..., description="Kakao's Profile Name")
    dog_name: str
    dog_gender: str = Field(..., description="남자아이/여자아이")
    dog_size: str = Field(..., description="소형견/중형견/대형견")
    dog_cuteness: int
    dog_breed: str = Field(..., example="푸들")    
    photo_path: Optional[str] = None
    birth_day: str
    current_weight: int
    past_weight: int
    weight_change: int = Field(..., description="체중 변화량")
    age: str = Field(..., example="1년 2개월")    
    # health_history: List[str] = Field(..., description="질병 이력 목록")
    # vaccinations: List[str] = Field(..., description="백신 접종 이력 목록")
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    dog_name: Optional[str] = None
    dog_gender: Optional[int] = Field(None, ge=0, le=1)
    dog_size: Optional[int] = Field(None, ge=0, le=2)
    dog_cuteness: Optional[int] = Field(None, ge=1, le=5)
    photo_path: Optional[str] = None
    birth_day: Optional[str] = Field(None, min_length=8, max_length=8, pattern=r"^\d{8}$")
    current_weight: Optional[int] = None
    past_weight: Optional[int] = None
    dog_breed: Optional[int] = None  # 품종 ID
    health_history: Optional[str] = None
    vaccinations: Optional[str] = None

    class Config:
        from_attributes = True

# 피드쪽 홈에서 노출되는 요소들
class UserProfileAbstract(BaseModel):
    pass
    # 강아지 이름 - dog_name
    # 품종 - dog_breed
    # 누적 산책 거리
    # 최고 랭킹
    # 배지
    # 방문자 리스트 -> 방문자 수
    # 한 줄 소개



# class Tag(BaseModel):
#     """
#     칭호 모델
#     """
#     name: str = Field(..., example="개귀여움")
#     description: str = Field(..., example="개귀여우면 획득")

# class ProfileResp(BaseModel):
#     """
#     프로필 리스폰스 모델
#     """
#     user_id: str = Field(..., example="changjjjjjjjj")
#     home_nickname: str = Field(..., example="멍멍홈")
#     nickname: str = Field(..., example="멍멍이")
#     kind: str = Field(..., example="이탈리안 하운드")
#     total_walked_dist: Optional[float] = Field(None, example=163.2)
#     best_rank: Optional[int] = Field(None, example=1)
#     visitors: int = Field(..., example=123456)
#     tags: Optional[List[Tag]] = Field(None, example=[
#         {"name": "개귀여움", "description": "개귀여우면 획득"},
#         {"name": "개빠름", "description": "개빠르면 획득"},
#         {"name": "개똑똑함", "description": "개똑똑하면 획득"},
#     ])
#     description: Optional[str] = Field(None, example="멍멍이는 멍멍 짖습니다.")
#     profile_image_url: Optional[HttpUrl] \
#         = Field(None, example="https://test.s3.amazonaws.com/test/test.jpg")

# class ProfileUpdateReq(BaseModel):
#     """
#     프로필 업데이트 요청 모델
#     """
#     home_nickname: str = Field(..., example="멍멍홈")
#     nickname: str = Field(..., example="멍멍이")
#     hide_walked_dist: bool = Field(..., example=False)
#     hide_best_rank: bool = Field(..., example=True)
#     tags: Optional[List[Tag]] = Field(None, example=[
#         {"name": "개귀여움", "description": "개귀여우면 획득"},
#         {"name": "개빠름", "description": "개빠르면 획득"},
#         {"name": "개똑똑함", "description": "개똑똑하면 획득"},
#     ])
#     description: Optional[str] = Field(None, example="멍멍이는 멍멍 짖습니다 2.")
#     profile_image_url: Optional[HttpUrl] \
#         = Field(None, example="https://test.s3.amazonaws.com/test/test2.jpg")

# class ProfileTagUpdateReq(BaseModel):
#     """
#     프로필 칭호 업데이트 요청 모델
#     """
#     tags: List[Tag] = Field(..., example=[
#         {"name": "개귀여움", "description": "개귀여우면 획득"},
#         {"name": "개빠름", "description": "개빠르면 획득"},
#         {"name": "개똑똑함", "description": "개똑똑하면 획득"},
#     ])

# class VisitorProfileResp(BaseModel):
#     """
#     방문자 프로필 리스폰스 모델
#     """
#     user_id: str
#     nickname: str
#     profile_image_url: Optional[HttpUrl]