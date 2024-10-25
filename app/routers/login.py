"""
유저관리의 로그인 관련 API
"""
from fastapi import HTTPException, Depends, APIRouter, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.responses import RedirectResponse, JSONResponse
import httpx, os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
from ..schemas.login import KaKaoUserInfo, TempUserCreate
from ..database.db import get_db
from ..services.login import create_temp_user, get_user_by_social_id, create_jwt_token

# 카카오 개발자 계정에서 얻은 정보로 설정
KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.environ.get("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI", "http://localhost:8000/user/login/auth")
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://kauth.kakao.com/oauth/authorize",
    tokenUrl="https://kauth.kakao.com/oauth/token",
)

router = APIRouter(
    prefix="/login",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("", summary="Login with Kakao")
async def login():
    """
    카카오 로그인을 위한 리다이렉트
    """
    return RedirectResponse(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )

# 카카오로부터 받은 인증 코드를 사용하여 access token을 얻음
@router.get("/auth", summary="Kakao Login Authorization Callback")
async def kakao_callback(code: str, request: Request, db: Session = Depends(get_db)):
    """
    OAuth2 인증 코드를 받아서 카카오 로그인 처리 \n
    이미 가입된 사용자인지 확인하고, 새 사용자라면 임시 사용자 생성 후 회원가입 프로세스로 리다이렉트 \n
    이미 가입된 사용자라면 로그인 처리 후 JWT 토큰 반환
    """
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
    user_info = await get_kakao_userinfo(access_token)
    
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
            "social_id" : temp_user.social_id,
            "name" : temp_user.name,
            "redirect_to": "/signup"
        })
    else:
        # 기존 사용자: 로그인 처리
        jwt_token = create_jwt_token({
            "sub": str(db_user.id),
            "social_id": db_user.social_id
        })
        return JSONResponse(content={
            "message": "User logged in successfully",
            "access_token": jwt_token,
            "token_type": "bearer"
        })

# access token을 사용하여 사용자 정보를 가져옴 
async def get_kakao_userinfo(token: str = Depends(oauth2_scheme), summary="Get Kakao User Info"):
    """
    발급받은 카카오 액세스 토큰을 사용하여 사용자 정보를 가져옴.
    """
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