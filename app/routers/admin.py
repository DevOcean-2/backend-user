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

@router.post("/disease", response_model=Disease, summary="Add New Disease")
async def add_disease(name: str, db: Session=Depends(get_db)):
    """
    강아지 질병 이름을 등록.
    """
    disease = create_disease(db, name)
    return Disease(id=disease.id, name=disease.name)

@router.delete("/disease/{disease_id}", summary="Delete Disease")
async def delete_disease(disease_id: int, db: Session = Depends(get_db)):
    """
    등록된 강아지 질병을 id로 삭제. \n
    성공시 200, {"message": "Successfully Deleted"} \n
    실패시 404, {"message": "No such Disease"}
    """
    result = delete_disease_by_id(db, disease_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Disease"}, status_code=404)

@router.post("/dogbreed", response_model=DogBreed, summary="Add New DogBreed")
async def add_dogbreed(name: str, db: Session=Depends(get_db)):
    """
    강아지 품종을 등록.
    """
    dog_breed = create_dogbreed(db, name)
    return DogBreed(id=dog_breed.id, name=dog_breed.name)

@router.delete("/dogbreed/{dogbreed_id}", summary="Delete DogBreed")
async def delete_dogbreed(dogbreed_id: int, db: Session = Depends(get_db)):
    """
    강아지 품종을 id로 삭제. \n
    성공시 200, {"message": "Successfully Deleted"} \n
    실패시 404, {"message": "No such dogbreed"}
    """
    result = delete_dogbreed_by_id(db, dogbreed_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such DogBreed"}, status_code=404)

@router.post("/vaccination", response_model=DogBreed, summary="Add New Vaccination")
async def add_vaccination(name: str, db: Session=Depends(get_db)):
    """
    강아지 백신을 등록.
    """
    vaccination = create_vaccination(db, name)
    return Vaccination(id=vaccination.id, name=vaccination.name)

@router.delete("/vaccination/{vaccination_id}", summary="Delete Vaccination")
async def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    """
    강아지 백신을 id로 삭제. \n
    성공시 200, {"message": "Successfully Deleted"} \n
    실패시 404, {"message": "No such Vaccination"}
    """
    result = delete_vaccination_by_id(db, vaccination_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Vaccination"}, status_code=404)

@router.post("/allergy", response_model=DogBreed, summary="Add New Allergy")
async def add_allergy(name: str, db: Session=Depends(get_db)):
    """
    강아지 알러지를 등록.
    """
    allergy = create_allergy(db, name)
    return Allergy(id=allergy.id, name=allergy.name)

@router.delete("/allergy/{allergy_id}")
async def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    """
    강아지 알러지를 id로 삭제. \n
    성공시 200, {"message": "Successfully Deleted"} \n
    실패시 404, {"message": "No such Allergy"}
    """
    result = delete_allergy_by_id(db, allergy_id)
    if result:
        return JSONResponse(content={"message": "Successfully Deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "No such Allergy"}, status_code=404)