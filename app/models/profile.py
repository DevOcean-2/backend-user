from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from ..database.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# User 상세 정보
class UserProfile(Base):
    __tablename__ = "users_profile"
    id = Column(Integer, primary_key=True, index=True)
    social_id = Column(String, ForeignKey("users.social_id"), unique=True)  # social_id로 외래키 설정
    dog_name = Column(String) # 이름
    dog_gender = Column(Integer) # 0: 수컷, 1: 암컷
    dog_size = Column(Integer) # 0: 소형견, 1: 중형견, 2: 대형견
    dog_cuteness = Column(Integer) # 귀여움 정도
    dog_breed = Column(Integer, ForeignKey("dog_breeds.id"))
    photo_path = Column(String) # 사진 경로
    birth_day = Column(String) # 생일
    current_weight = Column(Integer) # 현재 몸무게
    past_weight = Column(Integer) # 이전 몸무게
    health_history = Column(String) # 질병 이력 (리스트로 받아서 ,로 분리)
    vaccinations = Column(String) # 백신 이력 (리스트로 받아서 ,로 분리)

    user = relationship("User", back_populates="profile")
    breed = relationship("DogBreeds", back_populates="profiles")

class ProfileView(Base):
    __tablename__ = "profile_views"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.social_id"), nullable=False)
    visitor_id = Column(String, ForeignKey("users.social_id"), nullable=False)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 같은 User 테이블을 여러 foreign key로 참조하므로 foreign_keys가 필수
    owner = relationship("User", foreign_keys=[owner_id], back_populates="profile_viewers", lazy="joined")
    visitor = relationship("User", foreign_keys=[visitor_id], back_populates="viewed_profiles", lazy="joined")