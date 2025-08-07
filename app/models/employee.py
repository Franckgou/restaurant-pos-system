from app.core.database import Base
from sqlalchemy import  func, Integer, String, Boolean, DateTime
from app.core.database import TimestampMixin
from enum import Enum as PyEnum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from datetime import datetime

class RoleEnum(PyEnum):
    waiter = "waiter"
    cook  = "cook"
    busboy = "busboy"
    manager = "manager"

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable = False)
    name : Mapped[str]= mapped_column(String(50), nullable = False)
    role : Mapped[RoleEnum]= mapped_column(SQLEnum(RoleEnum), nullable = False)
    hashed_password : Mapped[str]= mapped_column(String, nullable = False)
    is_active : Mapped[bool]= mapped_column(Boolean, default = True)
    email : Mapped[str]= mapped_column(String(50), nullable = False, unique = True)
    employee_id : Mapped[str]= mapped_column(String, nullable = False, unique = True)
    last_login : Mapped[Optional[datetime]]= mapped_column(DateTime, nullable = True)
    login_count : Mapped[int]= mapped_column(Integer, default = 0)
    
    orders = relationship("Order", back_populates="employee")

  
