from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from app.crud.employee import get_employee_by_employee_id, update_last_login_and_login_count, get_employee_by_id, update_password
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.auth import ChangePassword 
from app.models.employee import Employee as EmployeeModel
auth_router = APIRouter(prefix ="/auth", tags=["Authentication"])


@auth_router.post("/login", response_model = LoginResponse)
def login( form_data : LoginRequest, db: Session = Depends(get_db) ) :
    
    employee = get_employee_by_employee_id(db, form_data.employee_id)

    if employee is None or not verify_password(form_data.password, employee.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail = "Incorrect employee ID or password",
                            headers={"WWW-Authenticate":"Bearer"},)
    access_token = create_access_token(data={"sub": str(employee.id), "role":employee.role.value})
    upadated_employee = update_last_login_and_login_count(db, employee)
    return LoginResponse(access_token= access_token,
                         token_type="bearer",
                         name=upadated_employee.name,
                         role = upadated_employee.role,
                         employee_id = upadated_employee.employee_id)

@auth_router.post("/change-password", response_model = dict)
def change_password(change_data : ChangePassword, db: Session = Depends(get_db), current_user: EmployeeModel = Depends(get_current_user)):

    if current_user is None or not verify_password(change_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST)
    updated_employee = update_password(db, current_user, change_data.new_password)

    return {"message": "Password updated successfully!"}