from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from app.models.models import Order, Status, User, UserToken


async def get_or_create_user(session: AsyncSession, user_id: int, username:str,phone_number:str):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        user = User(id=user_id, username=username, phone_number=phone_number,role='USER')
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def create_order(db: AsyncSession, order: Order):
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def read_orders_by_user_id(db: AsyncSession, user_id:int):
    stmt = await db.execute(select(Order).where(Order.user_id == user_id))
    result = stmt.scalars().all()
    return result

async def update_orders_status(db: AsyncSession, order_id:int, new_status: Status):
    stmt = await db.execute(select(Order).where(Order.id == order_id))
    result = stmt.scalars().first()

    if result is None:
        raise ValueError(f'Заказ {order_id} не найден')
    result.status = new_status
    await db.commit()
    return result

async def delete_orders_by_id(db: AsyncSession, order_id:int):
    stmt = await db.execute(delete(Order).where(Order.id == order_id))
    await db.commit()
