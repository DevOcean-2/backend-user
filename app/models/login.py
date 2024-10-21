from sqlalchemy import Boolean, Column, Integer, String
from ..database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    name = Column(String)
    social_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

class TempUser(Base):
    __tablename__ = "temp_users"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, index=True)
    name = Column(String)
    social_id = Column(String, index=True)

# User 상세 정보
class UserProfile(Base):
    __tablename__ = "users_profile"
    id = Column(Integer, primary_key=True, index=True)
    social_id = Column(String, index=True) # 로그인한 소셜 아이디
    dog_name = Column(String) # 이름
    dog_gender = Column(Integer) # 0: 수컷, 1: 암컷
    dog_size = Column(Integer) # 0: 소형견, 1: 중형견, 2: 대형견
    dog_breed = Column(String) # 품종
    dog_cuteness = Column(Integer) # 귀여움 정도
    photo_path = Column(String) # 사진 경로
    brith_day = Column(String) # 생일
    current_weight = Column(Integer) # 현재 몸무게
    past_weight = Column(Integer) # 이전 몸무게
    health_history = Column(String) # 질병 이력 (리스트로 받아서 ,로 분리)
    vaccinations = Column(String) # 백신 이력 (리스트로 받아서 ,로 분리)
    