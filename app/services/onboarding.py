from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ..models.onboarding import Disease as DiseaseTable
from ..models.onboarding import DogBreeds as DogBreedsTable
from ..models.onboarding import Vaccinations as VaccinationsTable
from ..models.onboarding import Allergies as AllergiesTable 
from ..schemas.onboarding import Disease, DogBreed, Vaccination, Allergy

load_dotenv()

# 질병 리스트 반환
def get_disease_list(db : Session):
    diseases = db.query(DiseaseTable).all()
    data = []
    for disease in diseases:
        data.append(
            Disease(
                id = disease.id,
                name = disease.name
            )
        )
    return data

# 질병 등록
def create_disease(db : Session, name : str):
    disease = DiseaseTable(name=name)
    db.add(disease)
    db.commit()
    db.refresh(disease)
    return disease

# 질병 ID로 삭제
def delete_disease_by_id(db: Session, disease_id: int) -> bool:
    disease = db.query(DiseaseTable).filter(DiseaseTable.id == disease_id).first()
    if disease:
        db.delete(disease)
        db.commit()
        return True
    return False

# 강아지 품종 리스트 반환
def get_dogbreed_list(db : Session):
    dogbreeds = db.query(DogBreedsTable).all()
    data = []
    for dogbreed in dogbreeds:
        data.append(
            DogBreed(
                id = dogbreed.id,
                name = dogbreed.name
            )
        )
    return data

# 강아지 품종 등록
def create_dogbreed(db : Session, name : str):
    dog_breed = DogBreedsTable(name=name)
    db.add(dog_breed)
    db.commit()
    db.refresh(dog_breed)
    return dog_breed

# 강아지 품종 ID로 삭제
def delete_dogbreed_by_id(db: Session, dogbreed_id: int) -> bool:
    dogbreed = db.query(DogBreedsTable).filter(DogBreedsTable.id == dogbreed_id).first()
    if dogbreed:
        db.delete(dogbreed)
        db.commit()
        return True
    return False

# 백신 리스트 반환
def get_vaccination_list(db : Session):
    vaccinations = db.query(VaccinationsTable).all()
    data = []
    for vaccination in vaccinations:
        data.append(
            Vaccination(
                id = vaccination.id,
                name = vaccination.name
            )
        )
    return data

# 백신 등록
def create_vaccination(db : Session, name : str):
    vaccination = VaccinationsTable(name=name)
    db.add(vaccination)
    db.commit()
    db.refresh(vaccination)
    return vaccination

# 백신 삭제
def delete_vaccination_by_id(db: Session, vaccination_id: int) -> bool:
    vaccination = db.query(VaccinationsTable).filter(VaccinationsTable.id == vaccination_id).first()
    if vaccination:
        db.delete(vaccination)
        db.commit()
        return True
    return False

# 백신 리스트 반환
def get_allergy_list(db : Session):
    allergies = db.query(AllergiesTable).all()
    data = []
    for allergy in allergies:
        data.append(
            Allergy(
                id = allergy.id,
                name = allergy.name
            )
        )
    return data

# 알러지 등록
def create_allergy(db : Session, name : str):
    allergy = AllergiesTable(name=name)
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy

# 알러지 삭제
def delete_allergy_by_id(db: Session, allergy_id: int) -> bool:
    allergy = db.query(DogBreedsTable).filter(DogBreedsTable.id == allergy_id).first()
    if allergy:
        db.delete(allergy)
        db.commit()
        return True
    return False