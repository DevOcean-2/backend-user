from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Disease(BaseModel):
    id : int
    name: str
    # description: Optional[str] = None
    
class DogBreed(BaseModel):
    id : int
    name: str
    # description: Optional[str] = None

class Vaccination(BaseModel):
    id : int
    name: str
    # description: Optional[str] = None

class Allergy(BaseModel):
    id : int
    name: str
    # description: Optional[str] = None