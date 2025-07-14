from app.core.database import Base
from sqlalchemy import Column, types,Integer, String, Boolean, DateTime
from app.core.database import TimestampMixin
from enum import Enum as PyEnum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

class RoleEnum(PyEnum):
    waiter = "waiter"
    cook  = "cook"
    busboy = "busboy"
    manager = "manager"

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String(50), nullable = False)
    role = Column(SQLEnum(RoleEnum), nullable = False)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean, default = True)
    email = Column(String(50), nullable = False, unique = True)
    employee_id = Column(String, nullable = False, unique = True)
    last_login = Column(DateTime, nullable = True)
    login_count = Column(Integer, default = 0)
    
    orders = relationship("Order", back_populates="employee")

  
