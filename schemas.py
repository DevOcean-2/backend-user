from pydantic import BaseModel
from typing import Optional

class TempUserCreate(BaseModel):
    # 카카오에서 넘어오는 값들로만 구성
    social_id: str
    name : str

class UserCreate(BaseModel):
    temp_user_id: int
    social_id: str
    name : str
    # 기본 필드, 선택 필드 추가될 예정

class User(BaseModel):
    id: int
    social_id: str
    name : str
    is_active: bool

    class Config:
        orm_mode = True

class TempUser(BaseModel):
    id: int
    social_id: str
    name : str

    class Config:
        orm_mode = True

class KaKaoUserInfo(BaseModel):
    id: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    profile_image: Optional[str] = None