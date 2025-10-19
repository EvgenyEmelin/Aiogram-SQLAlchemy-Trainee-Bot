from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from app.db.config import async_session_maker
from app.handlers.keyboard import reply_keyboard
from app.db.crud import create_order, get_or_create_user, read_orders_by_user_id
from app.models.models import Order, Status

router = Router()

class CreateOrder(StatesGroup):
    desc = State()

@router.message(CommandStart())
async def command_start(message: Message):
    async with async_session_maker() as session:
        await get_or_create_user(session, message.from_user.id, message.from_user.username, phone_number='')
    await message.answer('Приветствие. Краткая инструкция. Выбери кнопки ниже',reply_markup=reply_keyboard)

@router.message(F.text=='Создать заказ')
async def create_order_text(message: Message, state: FSMContext):
    await message.answer('Опишите какой заказ вы ходите совершить')
    await state.set_state(CreateOrder.desc)

@router.message(CreateOrder.desc)
async def create_order_state(message: Message,state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()

    user_id = message.from_user.id

    async with async_session_maker() as session:
        order = Order(user_id = user_id, description=data['desc'], status=Status.NEW)
        await create_order(session, order)

    await message.answer('Ваш заказ успешно создан')
    await state.clear()

@router.message(F.text=='Посмотреть мои заказы')
async def create_order_text(message: Message):
    user_id = message.from_user.id
    async with async_session_maker() as session:
        orders = await read_orders_by_user_id(session, user_id)
    if not orders:
        await message.answer('Увы, у Вас нет заказов!')
    else:
        response_text = 'Ваши заказы\n'
        for order in orders:
            response_text += f"- Заказ №{order.id}: {order.description}, статус: {order.status}\n"
        await message.answer(response_text)




