from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.users import Users
from auth import get_current_user, check_permission

router = APIRouter(tags=["business"])

MOCK_PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Телефон", "price": 30000},
]

MOCK_ORDERS = [
    {"id": 1, "product_id": 1, "quantity": 2},
    {"id": 2, "product_id": 2, "quantity": 1},
]

@router.get("/products")
async def get_products(db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)):
    if not await check_permission(user, "products", "read", db):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return MOCK_PRODUCTS

@router.post("/products")
async def create_product(db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)):
    if not await check_permission(user, "products", "create", db):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return {"message": "Товар создан", "product": {"id": 3, "name": "Новый товар", "price": 10000}}

@router.get("/orders")
async def get_orders(db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)):
    if not await check_permission(user, "orders", "read", db):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return MOCK_ORDERS

@router.post("/orders")
async def create_order(db: AsyncSession = Depends(get_session), user: Users = Depends(get_current_user)):
    if not await check_permission(user, "orders", "create", db):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return {"message": "Заказ создан", "order": {"id": 3, "product_id": 1, "quantity": 1}}
