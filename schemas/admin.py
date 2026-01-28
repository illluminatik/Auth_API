from pydantic import BaseModel
from typing import Optional

class BusinessElementCreate(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessElementResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class AccessRuleCreate(BaseModel):
    role_id: int
    element_id: int
    can_read: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class AccessRuleUpdate(BaseModel):
    can_read: Optional[bool] = None
    can_create: Optional[bool] = None
    can_update: Optional[bool] = None
    can_delete: Optional[bool] = None

class AccessRuleResponse(BaseModel):
    id: int
    role_id: int
    element_id: int
    can_read: bool
    can_create: bool
    can_update: bool
    can_delete: bool
    class Config:
        from_attributes = True
