from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session


from app.core.database import get_session
from app.models.employee import Employee
from app.models.Admin import Admin

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")

        if user_id is None or user_role is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = None
    if user_role == "admin":
        user = session.get(Admin, int(user_id))
    elif user_role == "employee":
        user = session.get(Employee, int(user_id))

    if user is None:
        raise credentials_exception

    return user



def require_admin_role(current_user: Admin = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return current_user



def require_employee_role(current_user: Employee = Depends(get_current_user)):
    if current_user.role != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return current_user