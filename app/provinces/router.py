from typing import Optional

from auth import get_api_key
from db.core import get_db
from exception import AlreadyExistsError, NotFoundError, ValidationError
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.params import Depends
from fastapi.security.api_key import APIKey
from fastapi_pagination import paginate
from pagination import DefaultPage
from provinces.models import DBProvince
from provinces.schema import CreateProvince, ReadProvince, UpdateProvince
from provinces.service import (
    _create_province,
    _update_province_by_id,
    read_province_by_id,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/provinces")

@router.get("/")
def get_provinces(
    request: Request,
    name: Optional[str] = None,
    region_id: Optional[int] = None,
    sort: Optional[str] = Query("name", description="Sort order: 'name' or '-name'"),
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
) -> DefaultPage[ReadProvince]:
    query = db.query(DBProvince)
    
    if name:
        query = query.filter(DBProvince.name.ilike(f"%{name}%"))
        
    if region_id:
        query = query.filter(DBProvince.region_id==region_id)
    
    if sort:
        if sort.startswith("-"):
            query = query.order_by(DBProvince.name.desc())
        else:
            query = query.order_by(DBProvince.name.asc())
    else:
        query = query.order_by(DBProvince.date_created.asc())
            
    provinces = query.all()
    provinces_list = [ReadProvince.from_orm(province) for province in provinces]
    return paginate(provinces_list)

@router.get("/{id}")
def get_province_by_id(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
) -> ReadProvince:
    try:
        db_province = read_province_by_id(id, db)
        return ReadProvince.from_orm(db_province)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
@router.post("/")
def create_province(
    request: Request,
    province: CreateProvince,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
) -> ReadProvince:
    try:
        created_province = _create_province(province, db)
        return ReadProvince.from_orm(created_province)
    except AlreadyExistsError as ie:
        raise HTTPException(detail=str(ie), status_code=400) from ie
    except ValidationError as ve:
        raise HTTPException(detail=str(ve), status_code=400) from ve
    
@router.put("/{id}")
def update_province_by_id(
    request: Request,
    id: int,
    province: UpdateProvince,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        updated_province = _update_province_by_id(id, province, db)
        return ReadProvince.from_orm(updated_province)
    except AlreadyExistsError as ie:
        raise HTTPException(
            detail=str(ie), 
            status_code=400
        ) from ie
    except ValidationError as ve:
        raise HTTPException(
            detail=str(ve),
            status_code=400
        ) from ve