from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class User(BaseModel):
    id: int
    social_id: str
    name : str
    is_active: bool
    # 기본 필드, 선택 필드 추가될 예정

    class Config:
        from_attributes = True

class TempUser(BaseModel):
    id: int
    social_id: str
    name : str

    class Config:
        from_attributes = True

class TempUserCreate(BaseModel):
    # 카카오에서 넘어오는 값들로만 구성
    social_id: str
    name : str

class UserCreate(BaseModel):
    temp_user_id : int
    social_id: str
    name : str

class KaKaoUserInfo(BaseModel):
    id: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    profile_image: Optional[str] = None