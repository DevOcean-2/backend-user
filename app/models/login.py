from sqlalchemy import Boolean, Column, Integer, String
from ..database.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    name = Column(String)
    social_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    profile_viewers = relationship("ProfileView", foreign_keys="ProfileView.owner_id", back_populates="owner", lazy="select") # 내 프로필을 본 사람들의 기록
    viewed_profiles = relationship("ProfileView", foreign_keys="ProfileView.visitor_id", back_populates="visitor", lazy="select") # 내가 본 다른 사람들의 프로필 기록

class TempUser(Base):
    __tablename__ = "temp_users"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, index=True)
    name = Column(String)
    social_id = Column(String, index=True)