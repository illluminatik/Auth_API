from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from models.users import Users
from models.auth import BlacklistedToken, AccessRule, BusinessElement
from fastapi.security import APIKeyHeader

SECRET_KEY = "meowmeowmeow"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(api_key_scheme), db: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token

    blacklist_result = await db.execute(select(BlacklistedToken).where(BlacklistedToken.token == clean_token))
    if blacklist_result.scalar_one_or_none():
        raise credentials_exception

    try:
        payload = jwt.decode(clean_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

def check_admin(user: Users = Depends(get_current_user)):
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(status_code=403, detail="Нужна роль admin")
    return user

async def check_permission(user: Users, element_name: str, action: str, db: AsyncSession):
    element_result = await db.execute(select(BusinessElement).where(BusinessElement.name == element_name))
    element = element_result.scalar_one_or_none()
    if not element:
        return False

    for role in user.roles:
        rule_result = await db.execute(
            select(AccessRule).where(AccessRule.role_id == role.id, AccessRule.element_id == element.id)
        )
        rule = rule_result.scalar_one_or_none()
        if rule:
            if action == "read" and rule.can_read:
                return True
            if action == "create" and rule.can_create:
                return True
            if action == "update" and rule.can_update:
                return True
            if action == "delete" and rule.can_delete:
                return True

    return False
