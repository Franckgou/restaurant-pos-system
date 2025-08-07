from app.core.database import TimestampMixin, Base
from pydantic import Field, BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum 
from app.schemas.mixins import TimestampMixinSchema

class RoleEnum(str, Enum):
    waiter = "waiter"
    cook = 'cook'
    busboy = "busboy"
    manager = "manager"


class EmployeeBase(BaseModel):
    employee_id : str = Field(description="The ID of the current employee")
    name : str = Field(min_length= 1, description = "The full name of the employee")
    email : str = Field(pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", description = "The employee email")
    is_active :  bool = Field(default= False, description = "the status at a time of an employee")
    role : RoleEnum = Field(description= "role of the employee")


    

class EmployeeCreate(EmployeeBase):
    password : str  = Field(description= "password of the employee")

class EmployeeUpdate(BaseModel):
    name : Optional[str] = Field(min_length=1, max_length=50)
    role : Optional[RoleEnum] = None
    email : Optional[str] = None
    is_active : Optional[bool] = None
    password : Optional[str] = Field(None, min_length=8, max_length=12, description="The new password of an employee")

    class Config:
        from_attributes = True
class Employee(EmployeeBase, TimestampMixinSchema):
    id : int = Field(description = "the database primary key ID of an employee")
    employee_id: str = Field(description = "The Unique ID of an employee, often generated")
    last_login: Optional[datetime] = None
    login_count: int = Field(default= 0)

    class Config:
        from_attributes = True
