from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from models.users import Users, Role
from models.auth import AccessRule, BusinessElement
from schemas.admin import AccessRuleCreate, AccessRuleUpdate, AccessRuleResponse, BusinessElementCreate, BusinessElementResponse
from auth import check_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/elements", response_model=list[BusinessElementResponse])
async def get_elements(db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    result = await db.execute(select(BusinessElement))
    return result.scalars().all()

@router.post("/elements", response_model=BusinessElementResponse)
async def create_element(data: BusinessElementCreate, db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    existing = await db.execute(select(BusinessElement).where(BusinessElement.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Такой элемент уже есть")

    element = BusinessElement(name=data.name, description=data.description)
    db.add(element)
    await db.commit()
    await db.refresh(element)
    return element

@router.get("/rules", response_model=list[AccessRuleResponse])
async def get_rules(db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    result = await db.execute(select(AccessRule))
    return result.scalars().all()

@router.post("/rules", response_model=AccessRuleResponse)
async def create_rule(data: AccessRuleCreate, db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    role = (await db.execute(select(Role).where(Role.id == data.role_id))).scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")

    element = (await db.execute(select(BusinessElement).where(BusinessElement.id == data.element_id))).scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="Элемент не найден")

    existing = await db.execute(select(AccessRule).where(AccessRule.role_id == data.role_id, AccessRule.element_id == data.element_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Такое правило уже есть")

    rule = AccessRule(
        role_id=data.role_id, element_id=data.element_id,
        can_read=data.can_read, can_create=data.can_create,
        can_update=data.can_update, can_delete=data.can_delete
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.patch("/rules/{rule_id}", response_model=AccessRuleResponse)
async def update_rule(rule_id: int, data: AccessRuleUpdate, db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    result = await db.execute(select(AccessRule).where(AccessRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Правило не найдено")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(rule, field, value)

    await db.commit()
    await db.refresh(rule)
    return rule

@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: int, db: AsyncSession = Depends(get_session), admin: Users = Depends(check_admin)):
    result = await db.execute(select(AccessRule).where(AccessRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Правило не найдено")

    await db.delete(rule)
    await db.commit()
    return {"message": "Удалено"}
