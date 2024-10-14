"""
유저관리의 로그인 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.responses import RedirectResponse, JSONResponse
import httpx, os, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
from schemas import KaKaoUserInfo, UserCreate, TempUserCreate
from database import get_db
from crud import create_user, create_temp_user, get_user_by_social_id, get_temp_user, delete_temp_user


# 카카오 개발자 계정에서 얻은 정보로 설정
KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.environ.get("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI", "http://localhost:8000/user/login/auth")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 30

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://kauth.kakao.com/oauth/authorize",
    tokenUrl="https://kauth.kakao.com/oauth/token",
)

router = APIRouter(
    prefix="/login",
    tags=["Login"],
    responses={404: {"description": "Not found"}},
)

# 사용자를 카카오 로그인 페이지로 redirect
@router.get("")
async def login():
    return RedirectResponse(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )

# 카카오로부터 받은 인증 코드를 사용하여 access token을 얻음
@router.get("/auth")
async def kakao_callback(code: str, request: Request, db: Session = Depends(get_db)):
    # 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "client_secret": KAKAO_CLIENT_SECRET,
        "code": code,
        "redirect_uri": KAKAO_REDIRECT_URI
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
    if response.status_code != 200:
        return JSONResponse(content={"error": "Failed to obtain access token"}, status_code=400)
    
    token_data = response.json()
    access_token = token_data["access_token"]

    # 카카오 액세스 토큰으로 사용자 정보 가져오기
    user_info = await get_user(access_token)
    
    # DB에서 사용자 확인
    db_user = get_user_by_social_id(db, social_id=user_info.id)
    
    if db_user is None:
        # 새 사용자: 임시 사용자 생성 및 회원가입 프로세스로 리다이렉트
        temp_user = TempUserCreate(
            social_id=user_info.id,
            name=user_info.nickname
        )
        temp_user_id = create_temp_user(db, temp_user)
        return JSONResponse(content={
            "message": "Additional information required",
            "temp_user_id": temp_user_id,
            "redirect_to": "/signup"
        })
    else:
        # 기존 사용자: 로그인 처리
        jwt_token = create_jwt_token({
            "sub": str(db_user.id),
            "email": db_user.email
        })
        return JSONResponse(content={
            "message": "User logged in successfully",
            "access_token": jwt_token,
            "token_type": "bearer"
        })

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

# access token을 사용하여 사용자 정보를 가져옴 
async def get_user(token: str = Depends(oauth2_scheme)):
    user_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(user_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not retrieve user info")
    
    user_data = response.json()
    
    # 필요한 정보 추출
    kakao_account = user_data.get('kakao_account', {})
    profile = kakao_account.get('profile', {})

    return KaKaoUserInfo(
        id=str(user_data.get('id')),
        email=kakao_account.get('email'),
        nickname=profile.get('nickname'),
        profile_image=profile.get('profile_image_url')
    )

# JWT 토큰 생성 함수
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
