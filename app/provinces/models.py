from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import BaseModel

class DBProvince(BaseModel):
    __tablename__ = "provinces"
    
    name = Column(String(50), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    
    region = relationship("DBRegion", back_populates="provinces")