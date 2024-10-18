"""
main.py
"""
import logging
import uuid
from fastapi import FastAPI, APIRouter
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette.responses import Response
from routers import login, onboarding, profile, admin

logger = logging.getLogger(__name__)

# fastAPI app 생성
app = FastAPI(
    title="Balbalm User Backend",
    description="backend for balbalm user service",
    version="1.0-beta",
    openapi_url="/openapi.json",
    debug=True
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

# user prefix 추가
user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)
admin_router = APIRouter(
    prefix='/admin',
    tags=["Admin"]
)

@user_router.get("", response_model=dict)
async def get_user_apis():
    """
    user 관련 모든 api 리스팅
    :return:
    """
    return {
        "message": "Welcome to the Balbalm User API!",
        "endpoints": {
            "GET /user/login" : "Kakao Social Login",
            "GET /user/login/auth" : "Kakao Login Authorization",
            "POST /user/onboarding/signup" : "Sign Up for New User",
            "GET /user/onboarding/dogbreed" : "Search DogBreed with Query",
            "POST /user/onboarding/dogbreed/add" : "Add New DogBreed",
            "PUT /user/profile": "Update your profile",
            "PUT /user/profile/tags": "Update your profile tags",
            "GET /user/profile/{user_id}": "Get user profile by user ID",
            "GET /user/profile/visitors": "Get your profile visitors",
        }
    }

user_router.include_router(login.router)
user_router.include_router(onboarding.router)
user_router.include_router(profile.router)
admin_router.include_router(admin.router)

# app 에 추가
app.include_router(user_router)
app.include_router(admin_router)