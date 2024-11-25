import logging
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette.responses import Response, JSONResponse
from app.routers import login, onboarding, profile, admin
from app.database.db import db_manager
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import os
from datetime import timedelta

class Settings(BaseModel):
    """
    AuthJWT config setting
    """
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "test_token")
    authjwt_access_token_expires: int = timedelta(days=7)       # 개발을 위해 7일로 늘림
    authjwt_refresh_token_expires: int = timedelta(days=7)      # 3일

@AuthJWT.load_config
def get_config():
    """
    AuthJWT config
    """
    return Settings()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 라이프사이클 이벤트 처리
    """
    # startup
    print("App Starting up...")
    db_manager.init_db()
    db_manager.create_tables()
    yield
    # shutdown
    if hasattr(db_manager, 'server') and db_manager.server:
        db_manager.server.stop()

# fastAPI app 생성
app = FastAPI(
    title="Balbalm User Backend",
    description="backend for balbalm user service",
    version="1.0-beta",
    openapi_url=None,  # 기본 openapi.json 경로 비활성화
    docs_url=None,     # 기본 /docs 경로 비활성화
    redoc_url=None,     # 기본 /redoc 경로 비활성화
    lifespan=lifespan
)

app.logger = logger

@app.middleware("http")
async def http_log(request, call_next):
    """
    로그
    :param request:
    :param call_next:
    :return:
    """
    response = await call_next(request)
    response_body = b''
    log_uuid = str(uuid.uuid1())[:8]
    # Combine async response chunk
    async for chunk in response.body_iterator:
        response_body += chunk
    logger.info("Log ID : %s - Request URL : %s %s",
                log_uuid, str(request.method), str(request.url))
    if "request_body" in context:
        logger.info("Log ID : %s - Request Body : %s", log_uuid, context["request_body"])
    logger.info("Log ID : %s - Response Body : %s", log_uuid, response_body)
    logger.info("Log ID : %s - Response Status Code : %s", log_uuid, str(response.status_code))

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

app.add_middleware(ContextMiddleware)

@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Health Check
    """
    return {"status": "ok"}

# Custom OpenAPI JSON 엔드포인트
@app.get("/user/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return JSONResponse(get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    ))

# Custom Swagger UI 엔드포인트
@app.get("/user/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/user/openapi.json",
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=None,
        init_oauth=None,
    )

# user prefix 추가
user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

admin_router = APIRouter(
    prefix='/admin',
    tags=["Admin"]
)

@user_router.get("", response_model=dict, summary="User API List")
async def get_user_apis():
    """
    USER 관련 모든 API 목록을 반환
    """
    return {
        "message": "Welcome to the Balbalm User API!",
        "endpoints": {
            "GET /user": "User API List",
            "GET /user/login": "Kakao Social Login",
            "GET /user/login/auth": "Kakao Login Authorization Callback",
            "POST /user/onboarding/signup": "Sign Up for New User",
            "GET /user/onboarding/dogbreed": "Get DogBreed List",
            "GET /user/onboarding/Disease": "Get Disease List",
            "GET /user/onboarding/vaccination": "Get Vaccination List",
            "GET /user/onboarding/allergy": "Get Allergy List",
            "GET /user/profiles/users": "Get Users List",
            "GET /user/profiles": "Get Profiles",
            "GET /user/profiles/{user_id}": "Get Profile",
            "PATCH /user/profiles/{user_id}": "Update Profile",
            "POST /user/profiles/visit": "Create Profile View",
            "GET /user/profiles/visitors/{user_id}": "Get Visitors"
        }
    }

user_router.include_router(login.router)
user_router.include_router(onboarding.router)
user_router.include_router(profile.router)

@admin_router.get("", response_model=dict, summary="Admin API List")
async def get_admin_apis():
    """
    ADMIN 관련 모든 API 목록을 반환
    """
    return {
        "message": "Welcome to the Balbalm Admin API!",
        "endpoints": {
            "POST /admin/disease": "Add New Disease",
            "DELETE /admin/disease/{disease_id}": "Delete Disease by ID",
            "POST /admin/dogbreed": "Add New DogBreed",
            "DELETE /admin/dogbreed/{dogbreed_id}": "Delete DogBreed by ID",
            "POST /admin/vaccination": "Add New Vaccination",
            "DELETE /admin/vaccination/{vaccination_id}": "Delete Vaccination by ID",
            "POST /admin/allergy": "Add New Allergy",
            "DELETE /admin/allergy/{allergy_id}": "Delete Allergy by ID",
        }
    }

admin_router.include_router(admin.router)

# app 에 추가
app.include_router(user_router)
app.include_router(admin_router)