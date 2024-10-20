"""
유저관리의 Admin 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Query
from starlette.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas.onboarding import Disease, DogBreed, Vaccination, Allergy
from ..database.db import get_db
from ..services.onboarding import (
    create_disease, delete_disease_by_id,
    create_dogbreed, delete_dogbreed_by_id,
    create_vaccination, delete_vaccination_by_id,
    create_allergy, delete_allergy_by_id
)

router = APIRouter(
    prefix="",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

# 강아지 질병 등록
@router.post("/disease", response_model=Disease)
async def add_disease(name: str, db: Session=Depends(get_db)):
    disease = create_disease(db, name)
    return Disease(id=disease.id, name=disease.name)

# 강아지 질병 삭제
@router.delete("/disease/{disease_id}")
async def delete_disease(disease_id: int, db: Session = Depends(get_db)):
    result = delete_disease_by_id(db, disease_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Disease"}, status_code=404)

# 강아지 품종 등록
@router.post("/dogbreed", response_model=DogBreed)
async def add_dogbreed(name: str, db: Session=Depends(get_db)):
    dog_breed = create_dogbreed(db, name)
    return DogBreed(id=dog_breed.id, name=dog_breed.name)

# 강아지 품종 삭제
@router.delete("/dogbreed/{dogbreed_id}")
async def delete_dogbreed(dogbreed_id: int, db: Session = Depends(get_db)):
    result = delete_dogbreed_by_id(db, dogbreed_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such DogBreed"}, status_code=404)

# 백신 등록
@router.post("/vaccination", response_model=DogBreed)
async def add_vaccination(name: str, db: Session=Depends(get_db)):
    vaccination = create_vaccination(db, name)
    return Vaccination(id=vaccination.id, name=vaccination.name)

# 백신 삭제
@router.delete("/vaccination/{vaccination_id}")
async def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    result = delete_vaccination_by_id(db, vaccination_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Vaccination"}, status_code=404)

# 알러지 등록
@router.post("/allergy", response_model=DogBreed)
async def add_allergy(name: str, db: Session=Depends(get_db)):
    allergy = create_allergy(db, name)
    return Allergy(id=allergy.id, name=allergy.name)

# 알러지 삭제
@router.delete("/allergy/{allergy_id}")
async def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    result = delete_allergy_by_id(db, allergy_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Allergy"}, status_code=404)