from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from models.auth import BlacklistedToken
from models.users import Users, Role
from schemas.users import UserCreate, UserResponse, UserLogin, Token, UserUpdate
from auth import create_access_token, get_current_user, check_admin, api_key_scheme
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Users).where(Users.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email занят")

    new_user = Users(
        name=user_data.name,
        surname=user_data.surname,
        middle_name=user_data.middle_name,
        email=user_data.email
    )
    new_user.set_password(user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Users).where(Users.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not user.check_password(form_data.password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Аккаунт деактивирован")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "refresh_token": "mock-refresh"}

@router.post("/logout")
async def logout(token: str = Depends(api_key_scheme), db: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
    db.add(BlacklistedToken(token=clean_token))
    await db.commit()
    return {"message": "Вы вышли"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
async def admin_data(admin: Users = Depends(check_admin)):
    return {"message": "Привет, админ!"}

@router.patch("/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, db: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/assign-role/{user_id}/{role_name}")
async def assign_role(user_id: int, role_name: str, db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    user = (await db.execute(select(Users).where(Users.id == user_id))).scalar_one_or_none()
    role = (await db.execute(select(Role).where(Role.name == role_name))).scalar_one_or_none()

    if not user or not role:
        raise HTTPException(status_code=404, detail="Не найдено")

    if role not in user.roles:
        user.roles.append(role)
        await db.commit()
    return {"message": f"Роль {role_name} назначена"}

@router.delete("/me")
async def delete_account(token: str = Depends(api_key_scheme), db: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
    db.add(BlacklistedToken(token=clean_token))
    current_user.is_active = False
    await db.commit()
    return {"message": "Аккаунт удален"}
