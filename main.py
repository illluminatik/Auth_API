from fastapi import FastAPI
from database import engine, Model, new_session
from contextlib import asynccontextmanager
from routers.users import router as users_router
from routers.business import router as business_router
from routers.admin import router as admin_router
from models.users import Role
from models.auth import BusinessElement, AccessRule
from sqlalchemy import select
import math

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    async with new_session() as session:
        async with session.begin():
            res = await session.execute(select(Role))
            if not res.scalars().first():
                session.add_all([Role(name="admin"), Role(name="user")])
                print("Роли созданы")

            res = await session.execute(select(BusinessElement))
            if not res.scalars().first():
                products = BusinessElement(name="products", description="Товары")
                orders = BusinessElement(name="orders", description="Заказы")
                session.add_all([products, orders])
                await session.flush()

                admin_role = (await session.execute(select(Role).where(Role.name == "admin"))).scalar_one()
                user_role = (await session.execute(select(Role).where(Role.name == "user"))).scalar_one()

                session.add_all([
                    AccessRule(role_id=admin_role.id, element_id=products.id, can_read=True, can_create=True, can_update=True, can_delete=True),
                    AccessRule(role_id=admin_role.id, element_id=orders.id, can_read=True, can_create=True, can_update=True, can_delete=True),
                    AccessRule(role_id=user_role.id, element_id=products.id, can_read=True, can_create=False, can_update=False, can_delete=False),
                    AccessRule(role_id=user_role.id, element_id=orders.id, can_read=True, can_create=False, can_update=False, can_delete=False),
                ])
                print("Элементы и правила созданы")

    print("БД готова")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(business_router)
app.include_router(admin_router)
