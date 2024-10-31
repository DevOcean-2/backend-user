from sqlalchemy import Boolean, Column, Integer, String
from ..database.db import Base
from sqlalchemy.orm import relationship

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # description = Column(String)
    
class DogBreeds(Base):
    __tablename__ = "dog_breeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # description = Column(String)

    profiles = relationship("UserProfile", back_populates="breed") # 역참조

class Vaccinations(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # description = Column(String)

class Allergies(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # description = Column(String)