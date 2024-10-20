import jwt, os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.login import User, TempUser, UserProfile
from ..schemas.login import UserCreate, TempUserCreate, UserProfileCreate
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 30

def get_user_by_social_id(db: Session, social_id: str):
    return db.query(User).filter(User.social_id == social_id).first()

def create_temp_user(db: Session, user: TempUserCreate):
    db_user = TempUser(
        name=user.name,
        social_id=user.social_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id

def get_temp_user(db: Session, temp_user_id: int):
    return db.query(TempUser).filter(TempUser.id == temp_user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        social_id=user.social_id,
        # 추후 기입 정보들의 필드로 추가될 예정
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_profile(db: Session, user: UserCreate, profile: UserProfileCreate):
    db_profile = UserProfile(
        social_id=user.social_id,
        dog_name=profile.dog_name,
        dog_gender=profile.dog_gender,
        dog_size=profile.dog_size,
        dog_breed=profile.dog_breed,
        dog_cuteness=profile.dog_cuteness,
        photo_path=profile.photo_path,
        brith_day=profile.brith_day,
        current_weight=profile.current_weight,
        past_weight=profile.past_weight,
        health_history=profile.health_history,
        vaccinations=profile.vaccinations
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_temp_user(db: Session, temp_user_id: int):
    db_temp_user = db.query(TempUser).filter(TempUser.id == temp_user_id).first()
    if db_temp_user:
        db.delete(db_temp_user)
        db.commit()
        return True
    return False

# JWT 토큰 생성 함수
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt