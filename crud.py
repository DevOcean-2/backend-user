from sqlalchemy.orm import Session
from models import User, TempUser
from schemas import UserCreate, TempUserCreate

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