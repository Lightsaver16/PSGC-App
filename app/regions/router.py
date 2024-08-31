from typing import Optional

from auth import get_api_key
from db.core import get_db
from exception import NotFoundError, RelatedEntityError, ValidationError
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.params import Depends
from fastapi_pagination import paginate
from fastapi.security.api_key import APIKey
from pagination import DefaultPage
from regions.models import DBRegion
from regions.schema import CreateRegion, ReadRegion, UpdateRegion
from regions.service import (
    _create_region,
    _update_region_by_id,
    read_region_by_id,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/regions")

@router.get("/")
def get_regions(
    request: Request,
    api_key: APIKey = Depends(get_api_key),
    name: Optional[str] = None,
    sort: Optional[str] = Query("name", description="Sort order: 'name' or '-name'"),
    db: Session = Depends(get_db)
) -> DefaultPage[ReadRegion]:
    query = db.query(DBRegion)
    
    if name:
        query = query.filter(DBRegion.name.ilike(f"%{name}%"))
        
    if sort:
        if sort.startswith("-"):
            query = query.order_by(DBRegion.name.desc())
        else:
            query = query.order_by(DBRegion.name.asc())
    else:
        query = query.order_by(DBRegion.date_created.asc())
        
    regions = query.all()
    regions_list = [ReadRegion.from_orm(region) for region in regions]
    return paginate(regions_list)

@router.get("/{id}")
def get_region_by_id(
    request: Request, 
    id: int, 
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
) -> ReadRegion:
    db_region = None
    try:
        db_region = read_region_by_id(id, db)
        return ReadRegion.from_orm(db_region)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    

@router.post("/")
def create_region(
    request: Request, 
    region: CreateRegion, 
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
) -> ReadRegion:
    try:
        db_region = _create_region(region, db)
        return ReadRegion.from_orm(db_region)
    except IntegrityError as e:
        raise HTTPException(detail="Region already exists.", status_code=400) from e
    except ValidationError as ve:
        raise HTTPException(detail=str(ve), status_code=400)
    
@router.put("/{id}")
def update_region_by_id(
    request: Request, 
    id: int, 
    region: UpdateRegion, 
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
) -> ReadRegion:
    try:
        updated_region = _update_region_by_id(id, region, db)
        return ReadRegion.from_orm(updated_region)
    except NotFoundError as er:
        raise HTTPException(detail=str(er), status_code=404) from er
    except IntegrityError as e:
        raise HTTPException(detail="Region already exists.", status_code=400) from e
    except ValidationError as ve:
        raise HTTPException(detail=str(ve), status_code=400) from ve