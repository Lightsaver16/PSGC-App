from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from provinces.models import DBProvince
from regions.schema import CreateRegion, UpdateRegion
from exception import NotFoundError, RelatedEntityError, ValidationError

from regions.models import DBRegion



def read_region_by_id(id, session: Session) -> DBRegion:
    region = session.query(DBRegion).filter(DBRegion.id==id).first()
    if region is None:
        raise NotFoundError(f"Region with id - {id} not found.")
    return region

def _create_region(region: CreateRegion, session: Session) -> DBRegion:
    if not region.name:
        raise ValidationError("Region name is required.")
    
    try:
        db_region = DBRegion(**region.model_dump())
        session.add(db_region)
        session.commit()
        session.refresh(db_region)
        return db_region
    except IntegrityError as e:
        session.rollback()
        raise e
    
def _update_region_by_id(id: int, region: UpdateRegion, session: Session) -> DBRegion:
    if not region.name:
        raise ValidationError("Region name is required.")
    
    db_region = read_region_by_id(id, session)
    for key, value in region.model_dump().items():
        setattr(db_region, key, value)
    session.commit()
    session.refresh(db_region)
    return db_region