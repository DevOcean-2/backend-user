from sqlalchemy import Boolean, Column, Integer, String
from ..database.db import Base

class DogBreeds(Base):
    __tablename__ = "dog_breeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # description = Column(String)

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