"""
Contains pydantic models - 
for serialization/deserialization of Province model.
"""
from pydantic import BaseModel

from provinces.models import DBProvince

class BaseProvince(BaseModel):
    name: str
    
class CreateProvince(BaseProvince):
    region_id: int

class UpdateProvince(BaseProvince):
    pass

class ReadProvince(BaseModel):
    id: int
    name: str
    region_id: int
    date_created: str
    date_updated: str
    
    @classmethod
    def from_orm(cls, orm_obj: DBProvince):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            region_id=orm_obj.region_id,
            date_created=orm_obj.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            date_updated=orm_obj.date_created.strftime("%Y-%m-%d %H:%M:%S")
        )