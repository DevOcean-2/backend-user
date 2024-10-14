"""
유저관리의 온보딩 관련 API
"""
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/onboarding",
    tags=["On-Boarding"],
    responses={404: {"description": "Not found"}},
)