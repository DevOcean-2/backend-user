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