"""
유저관리의 온보딩 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Query
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.db import get_db
from ..schemas.login import UserCreate
from ..schemas.profile import UserProfileCreate
from ..schemas.onboarding import Disease, DogBreed, Vaccination, Allergy
from ..services.login import create_user, get_temp_user, delete_temp_user, create_jwt_token
from ..services.onboarding import get_disease_list, get_dogbreed_list, get_vaccination_list, get_allergy_list
from ..services.profile import create_user_profile

router = APIRouter(
    prefix="/onboarding",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

# 새로 로그인 한 유저에 대해 회원가입 프로세스 진행
@router.post("/signup", summary="Sign Up for New User")
async def complete_signup(user_data: UserCreate, user_profile_data: UserProfileCreate, db: Session = Depends(get_db)):
    """
    Complete the sign-up process for a new user.
    /user/login/auth API를 통해 받은 사용자 정보를 이용하여 회원가입을 완료
    """
    # 임시 사용자 정보 확인
    temp_user = get_temp_user(db, user_data.temp_user_id)
    if not temp_user:
        raise HTTPException(status_code=400, detail="Invalid temp_user_id")
    
    # 새 사용자 생성
    new_user = UserCreate(
        # TempUser에서 가져온 필드값들
        temp_user_id = temp_user.id,
        social_id=temp_user.social_id,
        name=temp_user.name,
    )

    db_user = create_user(db, new_user)
    db_user_profile = create_user_profile(db, new_user, user_profile_data)

    # 임시 사용자 정보 삭제
    delete_temp_user(db, temp_user.id)
    
    # JWT 토큰 생성
    jwt_token = create_jwt_token({
        "sub": str(db_user.id),
        "social_id": db_user.social_id
    })
    
    return JSONResponse(content={
        "message": "User registered successfully",
        "access_token": jwt_token,
        "token_type": "bearer"
    })


@router.get("/dogbreed", response_model=List[DogBreed], summary="Get DogBreed List")
async def search_dogbreed(db: Session=Depends(get_db)):
    """
    품종 전체를 리스트로 반환.
    """
    breeds = get_dogbreed_list(db)
    return breeds

@router.get("/disease", response_model=List[Disease], summary="Get Disease List")
async def search_disease(db: Session=Depends(get_db)):
    """
    질병 전체를 리스트로 반환.
    """
    diseases = get_disease_list(db)
    return diseases

@router.get("/vaccination", response_model=List[Vaccination], summary="Get Vaccination List")
async def search_vaccination(db: Session=Depends(get_db)):
    """
    백신 전체를 리스트로 반환.
    """
    vaccines = get_vaccination_list(db)
    return vaccines

@router.get("/allergy", response_model=List[Allergy], summary="Get Allergy List")
async def search_allergy(db: Session=Depends(get_db)):
    """
    알러지 전체를 리스트로 반환.
    """
    allergies = get_allergy_list(db)
    return allergies