from sqlalchemy.orm import Session

from provinces.schema import CreateProvince, UpdateProvince
from exception import AlreadyExistsError, NotFoundError, ValidationError
from provinces.models import DBProvince

def read_province_by_id(id: int, session: Session):
    province = session.query(DBProvince).filter(DBProvince.id==id).first()
    if province is None:
        raise NotFoundError(f"Province with id - {id} not found.")
    return province

def _create_province(province: CreateProvince, session: Session) -> DBProvince:
    validation_errors = []
    if province_exists_on_create(province, session):
        raise AlreadyExistsError("Province already exists.")
    
    if not province.name:
        validation_errors.append(dict(
            name = "Name is required."
        ))
        
    if not province.region_id:
        validation_errors.append(dict(
            region_id = "Region id is required."
        ))
    
    if validation_errors:
        raise ValidationError(dict(
            errors = validation_errors
        ))
    
    db_province = DBProvince(**province.model_dump())
    session.add(db_province)
    session.commit()
    session.refresh(db_province)
    return db_province

def province_exists_on_create(province: CreateProvince, session: Session) -> bool:
    existing_province = session.query(DBProvince).filter(
        DBProvince.region_id==province.region_id, 
        DBProvince.name==province.name
    ).first()
    return existing_province is not None

def _update_province_by_id(
    id: int, 
    province: UpdateProvince, 
    session: Session
) -> DBProvince:
    if not province.name:
        raise ValidationError("Province name is required.")
    
    if province_exists_on_update(id, province, session):
        raise AlreadyExistsError("Province already exists.")
    
    db_province = read_province_by_id(id, session)
    for key, value in province.model_dump().items():
        setattr(db_province, key, value)
    session.commit()
    session.refresh(db_province)
    return db_province

def province_exists_on_update(
    id: int, 
    province: UpdateProvince, 
    session: Session
) -> bool:
    existing_province = session.query(DBProvince).filter(
        DBProvince.name==province.name,
        DBProvince.id != id
    ).first()
    return existing_province is not None