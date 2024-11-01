from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
from dotenv import load_dotenv
from ..schemas.profile import UserProfileCreate, UserProfileResponse, UserProfileUpdate
from ..schemas.login import UserCreate
from ..schemas.profile import ProfileViewBase, ProfileViewer
from ..models.profile import UserProfile, ProfileView
from ..models.login import User
from ..models.onboarding import DogBreeds
from dateutil.relativedelta import relativedelta
from datetime import datetime
load_dotenv()

def create_user_profile(db: Session, user: UserCreate, profile: UserProfileCreate):
    db_profile = UserProfile(
        social_id=user.social_id,
        dog_name=profile.dog_name,
        dog_gender=profile.dog_gender,
        dog_size=profile.dog_size,
        dog_breed=profile.dog_breed,
        dog_cuteness=profile.dog_cuteness,
        photo_path=profile.photo_path,
        birth_day=profile.birth_day,
        current_weight=profile.current_weight,
        past_weight=profile.past_weight,
        health_history=profile.health_history,
        vaccinations=profile.vaccinations
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# 모든 사용자들의 ID를 반환
def get_users(db:Session):
    users = db.query(User).all()
    return users

def get_user_by_id(db:Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 특정 ID의 사용자의 Profile을 반환
def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first() # user_id로 User 객체 찾아서 social_id, name 추출
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = db.query(UserProfile).filter(UserProfile.social_id == user.social_id).first() # social_id로 UserProfile 객체 찾기
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    dog_breed = db.query(DogBreeds).filter(DogBreeds.id == profile.dog_breed).first() # UserProfile의 dog_breed의 id값으로 품종 이름 추출
    if not dog_breed:
        raise HTTPException(status_code=404, detail="DogBreed not found")

    # 날짜 계산
    birth = datetime.strptime(profile.birth_day, "%Y%m%d")
    diff = relativedelta(datetime.now(), birth)
    
    size_map = {0: "소형견", 1: "중형견", 2: "대형견"}
    profile_response = UserProfileResponse(
        user_name=user.name,
        dog_name=profile.dog_name,
        dog_gender="남자아이" if profile.dog_gender == 0 else "여자아이",
        dog_size=size_map.get(profile.dog_size, "알 수 없음"),
        dog_cuteness=profile.dog_cuteness,
        dog_breed=dog_breed.name,
        photo_path=profile.photo_path,
        birth_day=profile.birth_day,
        current_weight=profile.current_weight,
        past_weight=profile.past_weight,
        weight_change=profile.current_weight-profile.past_weight,
        age=f"{diff.months}개월" if diff.years == 0 else f"{diff.years}년 {diff.months}개월",
        # health_history=profile.health_history,
        # vaccinations=profile.vaccinations
    )
    return profile_response

# 특정 사용자의 프로필 수정(일부 수정 가능)
def update_user_profile(db: Session, user_id: int, profile_update: UserProfileUpdate):
    # 기존 프로필 조회
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = db.query(UserProfile).filter(UserProfile.social_id == user.social_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # 업데이트할 데이터 준비
    update_data = profile_update.dict(exclude_unset=True)  # 설정된 필드만 포함
    
    # 각 필드 업데이트
    for field, value in update_data.items():
        if value is not None:  # None이 아닌 값만 업데이트
            setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    # 업데이트된 프로필 반환
    return get_user_profile(db, user_id) # 수정된 사항 확인할 수 있도록

def create_view(db: Session, view:ProfileViewBase):
    db_view = ProfileView(**view.dict())
    db.add(db_view)
    db.commit()
    db.refresh(db_view)
    return db_view

def get_visitor_lists(db: Session, user_id : int):
    results = (
        db.query(
            ProfileView.visitor_id,
            User.name.label('visitor_name'),
            # User.image.label('visitor_image'), # 나중에 유저 프로필 사진 등록시 같이 추가할 예정
            ProfileView.viewed_at
        )
        .join(User, User.id == ProfileView.visitor_id)
        .filter(ProfileView.owner_id == user_id)
        .order_by( 
            ProfileView.visitor_id,             # visitor_id로 그룹핑
            ProfileView.viewed_at.desc()        # 같은 visitor_id 내에서 최신순 정렬
        )
        .distinct(ProfileView.visitor_id)       # visitor_id 별로 최신 조회 기록만 선택
        .order_by(ProfileView.viewed_at.desc()) # 최종 결과를 다시 최신순 정렬
        .all()
    )

    return [
        ProfileViewer(
            visitor_id=row.visitor_id,
            visitor_name=row.visitor_name,
            # visitor_image=row.visitor_image,
            viewed_at=row.viewed_at
        )
        for row in results
    ]