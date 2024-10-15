"""
유저관리의 온보딩 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Query
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas import UserCreate, DogBreed
from database import get_db
from crud import create_user, get_temp_user, delete_temp_user, create_jwt_token, get_dogbreed_list, create_dogbreed


router = APIRouter(
    prefix="/onboarding",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

# 새로 로그인 한 유저에 대해 회원가입 프로세스 진행
@router.post("/signup")
async def complete_signup(user_data: UserCreate, db: Session = Depends(get_db)):
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

        # 새로 입력 받은 필드 값들
        # 추후 추가 예정
    )
    db_user = create_user(db, new_user)
    
    # 임시 사용자 정보 삭제
    delete_temp_user(db, temp_user.id)
    
    # JWT 토큰 생성
    jwt_token = create_jwt_token({
        "sub": str(db_user.id),
    })
    
    return JSONResponse(content={
        "message": "User registered successfully",
        "access_token": jwt_token,
        "token_type": "bearer"
    })

@router.post("/dogbreed/add", response_model=DogBreed)
async def add_dogbreed(name: str, db: Session=Depends(get_db)):
    dog_breed = create_dogbreed(db, name)
    return DogBreed(id=dog_breed.id, name=dog_breed.name)

@router.get("/dogbreed", response_model=List[DogBreed])
async def search_dogbreed(query: str = Query(..., min_length=1), db: Session=Depends(get_db)):
    breeds = get_dogbreed_list(db, query) # query를 포함하는 품종 리스트 반환
    return breeds