from app.core.database import get_db
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.crud.employee import get_employee_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    

    employee_id = int(payload["sub"])
    employee = get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not employee.is_active:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    return employee