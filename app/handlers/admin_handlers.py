import os
import json

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types.message import Message
from sqlalchemy import select, func
from app.db.config import async_session_maker
from app.db.crud import update_orders_status
from app.models.models import User, Status
from dotenv import load_dotenv

load_dotenv()
admins_str = os.getenv("ADMINS", "")
admin_ids = set()
if admins_str:
    admin_ids = set(int(admin_id) for admin_id in admins_str.split(",") if admin_id.strip().isdigit())

def is_admin(user_id: int) -> bool:
    return user_id in admin_ids

admin_router = Router()

@admin_router.message(F.text == 'Админ-панель')
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Доступ запрещен")
        return

    async with async_session_maker() as session:
        user_count = await session.execute(select(func.count(User.id)).select_from(User))
        count = user_count.scalar()
    await message.answer(f"👥 В базе {count} пользователей\n")

@admin_router.message(Command('changestatusorder'))
async def change_status_order(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Доступ запрещен")
        return

    parts = message.text.split(' ')
    if len(parts) < 3:
        await message.answer("Используйте: /changestatusorder <order_id> <new_status>")
        return

    try:
        order_id = int(parts[1])
        new_status = Status[parts[2].upper()]
    except (ValueError, KeyError):
        await message.reply('Ошибка в формате order_id или статусе')
        return

    async with async_session_maker() as session:
        try:
            order = await update_orders_status(session, order_id, new_status)
            await message.answer(f"Статус заказа #{order_id} изменён на {new_status.name}")
        except Exception as e:
            await message.reply(f'Ошибка при изменении статуса {str(e)}')
