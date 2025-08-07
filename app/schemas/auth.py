from pydantic import BaseModel, constr
from app.models.employee import RoleEnum


class LoginRequest(BaseModel):
    employee_id : str
    password : str

class LoginResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"
    name : str
    role : RoleEnum
    employee_id : str

class TokenData(BaseModel):
    employee_id : str
    role : RoleEnum

class ChangePassword(BaseModel):
    current_password :str
    new_password : str



