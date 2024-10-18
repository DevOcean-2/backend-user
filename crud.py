import jwt, os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User, TempUser, DogBreeds, Vaccinations, Allergies 
from schemas import UserCreate, TempUserCreate
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

# 강아지 품종 리스트 반환
def get_dogbreed_list(db : Session):
    dogbreeds = db.query(DogBreeds).all()
    return dogbreeds

# 강아지 품종 등록
def create_dogbreed(db : Session, name : str):
    dog_breed = DogBreeds(name=name)
    db.add(dog_breed)
    db.commit()
    db.refresh(dog_breed)
    return dog_breed

# 강아지 품종 ID로 삭제
def delete_dogbreed_by_id(db: Session, dogbreed_id: int) -> bool:
    dogbreed = db.query(DogBreeds).filter(DogBreeds.id == dogbreed_id).first()
    if dogbreed:
        db.delete(dogbreed)
        db.commit()
        return True
    return False

# 백신 리스트 반환
def get_vaccination_list(db : Session):
    vaccinations = db.query(Vaccinations).all()
    return vaccinations

# 백신 등록
def create_vaccination(db : Session, name : str):
    vaccination = Vaccinations(name=name)
    db.add(vaccination)
    db.commit()
    db.refresh(vaccination)
    return vaccination

# 백신 삭제
def delete_vaccination_by_id(db: Session, vaccination_id: int) -> bool:
    vaccination = db.query(Vaccinations).filter(Vaccinations.id == vaccination_id).first()
    if vaccination:
        db.delete(vaccination)
        db.commit()
        return True
    return False

# 백신 리스트 반환
def get_allergy_list(db : Session):
    allergies = db.query(Allergies).all()
    return allergies

# 알러지 등록
def create_allergy(db : Session, name : str):
    allergy = Allergies(name=name)
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy

# 알러지 삭제
def delete_allergy_by_id(db: Session, allergy_id: int) -> bool:
    allergy = db.query(DogBreeds).filter(DogBreeds.id == allergy_id).first()
    if allergy:
        db.delete(allergy)
        db.commit()
        return True
    return False