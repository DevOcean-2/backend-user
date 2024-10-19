from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.onboarding import DogBreeds, Vaccinations, Allergies 
from dotenv import load_dotenv
load_dotenv()

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