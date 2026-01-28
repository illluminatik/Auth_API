from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    surname: str
    middle_name: Optional[str] = None
    email: EmailStr
    password: str
    password_repeat: str

    @validator('password_repeat')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    middle_name: Optional[str] = None
    email: EmailStr
    is_active: bool
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
