from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List, Optional
from datetime import datetime

from app.models.employee import Employee as EmployeeModel, RoleEnum

from app.schemas.employee import EmployeeCreate, EmployeeUpdate

from app.core.security import hash_password, verify_password

#helper functions
def _get_employee_by_attribute(db: Session, attribute: str, value) -> Optional[EmployeeModel]:
    return db.query(EmployeeModel).filter(getattr(EmployeeModel, attribute) == value).first()

def check_employee_id_exists(db:Session, employee_id: str) -> bool:
    return _get_employee_by_attribute(db, "employee_id", employee_id) is not None

def check_email_exists(db:Session, email:str) -> bool:
    return _get_employee_by_attribute(db, "email", email) is not None

def update_password(db: Session, employee: EmployeeModel, new_password:str) -> EmployeeModel:
    employee.hashed_password = hash_password(new_password)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

# Authentification
def get_employee_by_employee_id(db:Session, employee_id: str) -> Optional[EmployeeModel]:
    return _get_employee_by_attribute(db, "employee_id", employee_id)

def get_employee_by_email(db:Session, email:str) :
    return _get_employee_by_attribute(db, "email", email)

def update_last_login_and_login_count(db:Session, employee: EmployeeModel):
    employee.last_login = datetime.utcnow()
    employee.login_count = (employee.login_count or 0) + 1
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

# Employee Management functions
def create_employee(db:Session, employee: EmployeeCreate) -> Optional[EmployeeModel]:
    if check_employee_id_exists(db, employee.employee_id):
        raise ValueError("Employee ID already exists.")
    if check_email_exists(db, employee.email):
        raise ValueError("Email already exists.")
    
    hashed_password = hash_password(employee.password)
    db_employee = EmployeeModel(
        employee_id = employee.employee_id,
        name = employee.name,
        email = employee.email,
        is_active = employee.is_active,
        role = employee.role,
        hashed_password = hashed_password, 
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except exc.IntegrityError:
        db.rollback()
        raise ValueError("Database Intergrity error, possibly duplicate ID/email")
    
def get_employee_by_id(db:Session, id : int) -> Optional[EmployeeModel]:
    return db.query(EmployeeModel).filter(EmployeeModel.id == id).first()

def get_all_employees(db:Session, skip: int = 0, limit: int=100) -> List[EmployeeModel]:
    return db.query(EmployeeModel).offset(skip).limit(limit).all()

def update_employee(db:Session, employee: EmployeeModel, employee_update: EmployeeUpdate) -> EmployeeModel:
    if employee_update.email is not None and employee_update.email != employee.email:
        if check_email_exists(db, employee_update.email):
            raise ValueError("New email already exists for another employee.")
        
    update_data = employee_update.model_dump(exclude_unset= True)

    for field, value in update_data.items():
        if field == "password" and value is not None:
            employee.hashed_password = hash_password(value)
        elif field != "employee_id":
            setattr(employee, field, value)
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def soft_delete_employee(db: Session, employee: EmployeeModel) -> EmployeeModel:
    if employee.is_active:
        employee.is_active = False
        db.add(employee)
        db.commit()
        db.refresh(employee)
    return employee