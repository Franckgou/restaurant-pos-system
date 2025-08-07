from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.employee import EmployeeCreate, Employee, EmployeeUpdate
from app.core.database import get_db
from app.models.employee import Employee as EmployeeModel, RoleEnum
from app.api.deps import get_current_user
from app.crud.employee import create_employee, get_employee_by_employee_id, get_all_employees, update_employee, soft_delete_employee

employee_router = APIRouter(prefix = "/employees", tags = ["Employees"])

@employee_router.post("/", response_model = Employee, status_code = status.HTTP_201_CREATED)
def add(employee: EmployeeCreate, db: Session = Depends(get_db),  current_user : EmployeeModel = Depends(get_current_user) ):
    if current_user.role != RoleEnum.manager:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    try:
        new_employee = create_employee(db, employee)
    except ValueError:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST)
    return new_employee

@employee_router.get("/{employee_id}", response_model = Employee)
def get_single(employee_id : str, db: Session = Depends(get_db), current_user: EmployeeModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.manager and current_user.employee_id != employee_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform such task")

    employee = get_employee_by_employee_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return employee

@employee_router.get("/", response_model = List[Employee])
def get_all(skip : int = 0, limit : int = 100, db: Session = Depends(get_db), current_user : EmployeeModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.manager:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    all_employees = get_all_employees(db, skip, limit)
    return all_employees

@employee_router.put("/{employee_id}", response_model= Employee)
def update_single(employee_id: str, employee_update: EmployeeUpdate, db: Session = Depends(get_db), current_user: EmployeeModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.manager:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "you can not perfom suvh task")
    
    employee = get_employee_by_employee_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    try :
        updated_employee = update_employee(db, employee, employee_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = str(e))
    return updated_employee
    
@employee_router.delete("/{employee_id}")
def delete(employee_id : str, db: Session = Depends(get_db), current_user: EmployeeModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.manager:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "you don't have the right to perform such task")

    employee = get_employee_by_employee_id(db, employee_id) 
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
           
    soft_delete_employee(db, employee)
    return {"message": "Employee deactivated successfully"}