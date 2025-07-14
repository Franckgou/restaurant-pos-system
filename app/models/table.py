from sqlalchemy import Column, Integer, String, Boolean, DateTime
from enum import Enum as PyEnum
from app.core.database import Base, TimestampMixin
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

class TableStatus(PyEnum):
    clean = "clean"
    occupied = "occupied"
    dirty = "dirty"
    inactive = "inactive"

class Table(Base, TimestampMixin):
    __tablename__  = "tables"
    id = Column(Integer, primary_key= True, nullable = False)
    capacity = Column(Integer, nullable = False)
    status = Column(SQLEnum(TableStatus), nullable = False)
    last_cleaned = Column(DateTime, nullable = False)
    table_id = Column(String, nullable = False, unique = True)
    
    orders = relationship("Order", back_populates= "table")
