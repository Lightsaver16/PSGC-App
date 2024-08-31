from sqlalchemy import Column, String
from models import BaseModel
from sqlalchemy.orm import relationship


class DBRegion(BaseModel):
    __tablename__ = "regions"
    
    name = Column(String(50), unique=True, nullable=False)
    provinces = relationship("DBProvince", back_populates="region")