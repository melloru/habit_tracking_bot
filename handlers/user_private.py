from aiogram import types, Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from kbds.reply import get_keyboard
from database.orm_query import orm_add_habit

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter('private'))

start_kb = get_keyboard('Меню',
                        'Помощь',
                        'Привычки',
                        'Задачи',
                        sizes=(2,),
                        placeholder='Что Вас интересует?'
                        )


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Команда старт', reply_markup=start_kb)


@user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(Command('menu'))  # Тут будет выпадающее меню с функциями(привычка - создать, задача - создать)
async def start_cmd(message: types.Message):
    await message.answer('Команда меню')


# @user_private_router.message(F.text.lower() == 'помощь')
# @user_private_router.message(Command('help'))  # Тут будет выпадающее меню с объяснением каждой функции. ТехПоддержка
# async def start_cmd(message: types.Message):
#     await message.answer('Команда помощь')

class AddHabit(StatesGroup):
    name = State()
    time = State()
    test = State()

    texts = {
        'AddHabit:name': 'Введите название заново',
        'AddHabit:time': 'Введите время заново',
        'AddHabit:test': 'Введите test заново',
    }

@user_private_router.message(StateFilter('*'), Command('cancel'))
@user_private_router.message(StateFilter('*'), F.text.lower() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer('Действия отменены', reply_markup=start_kb)


@user_private_router.message(StateFilter('*'), Command('back'))
@user_private_router.message(StateFilter('*'), F.text.lower() == 'назад')
async def back_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state == AddHabit.name:
        await message.answer('Предидущего шага нет, напишите "отмена".')
        return

    previous = None
    for step in AddHabit.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Вы вернулись к прошлому шагу\n{AddHabit.texts[previous.state]}')
            return
        previous = step



@user_private_router.message(F.text.lower() == 'привычки')
@user_private_router.message(Command('habits'))  # Выводит список привычек с привязанными кнопками к карточке(изменить, удалить). Поддерживает пагинацию.
async def habit(message: types.Message):
    await message.answer('habits', reply_markup=get_keyboard('Добавить привычку', 'Показать привычки'))


@user_private_router.message(StateFilter(None), F.text == 'Добавить привычку')
async def add_habit(message: types.Message, state: FSMContext):
    await message.answer('Введите название привычки', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddHabit.name)


@user_private_router.message(AddHabit.name, F.text)
async def add_habit_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите кол-во дней')
    await state.set_state(AddHabit.time)


# @user_private_router.message(AddHabit.time, F.text)
# async def add_habit_time(message: types.Message, state: FSMContext):
#     await state.update_data(time=message.text)
#     await message.answer('Привычка успешно добавлена!', reply_markup=start_kb)
#     data = await state.get_data()
#     await message.answer(str(data))
#     await state.clear()

@user_private_router.message(AddHabit.test, F.text)
async def add_habit_time(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(test=message.text)

    data = await state.get_data()
    await orm_add_habit(session, data)
    await message.answer('Привычка успешно добавлена!', reply_markup=start_kb)

    await message.answer(f'{str(data)=}')
    await state.clear()





# @user_private_router.message(F.text.lower() == 'задачи')
# @user_private_router.message(Command('tasks'))  # Выводит список задач с привязанными кнопками к карточке(изменить, удалить). Поддерживает пагинацию.
# async def start_cmd(message: types.Message):
#     await message.answer('tasks')

# @user_private_router.message(Command(''))
# async def start_cmd(message: types.Message):
#     await message.answer('')
#
#
# @user_private_router.message(Command(''))
# async def start_cmd(message: types.Message):
#     await message.answer('')
