"""
Contains pydantic models - 
for serialization/deserialization of Region model.
"""
from pydantic import BaseModel

from regions.models import DBRegion


class BaseRegion(BaseModel):
    name: str
    
class CreateRegion(BaseRegion):
    pass

class UpdateRegion(BaseRegion):
    pass

class ReadRegion(BaseModel):
    id: int
    name: str
    date_created: str
    date_updated: str
    
    @classmethod
    def from_orm(cls, orm_obj: DBRegion):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            date_created=orm_obj.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            date_updated=orm_obj.date_created.strftime("%Y-%m-%d %H:%M:%S")
        )