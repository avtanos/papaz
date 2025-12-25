from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.cashier import Cashier

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_cashier(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Cashier:
    """Получение текущего авторизованного кассира"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    cashier = db.query(Cashier).filter(Cashier.username == username).first()
    if cashier is None:
        raise credentials_exception
    
    if not cashier.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cashier account is inactive"
        )
    
    return cashier


async def get_current_active_cashier(
    current_cashier: Cashier = Depends(get_current_cashier)
) -> Cashier:
    """Проверка что кассир активен"""
    if not current_cashier.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cashier account is inactive"
        )
    return current_cashier

