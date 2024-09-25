from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

from crud_functions import initiate_db, get_all_pictures, add_user, is_included

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Определяем состояния
class AuthStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()
    waiting_for_password_confirmation = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Вход')
button2 = KeyboardButton(text='Регистрация')
button3 = KeyboardButton(text='Информация')
kb.insert(button)
kb.insert(button2)
kb.insert(button3)


kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data="calories")
button_in2 = InlineKeyboardButton(text='Формулы расчёта', callback_data="formulas")
kb_in.insert(button_in)
kb_in.insert(button_in2)


kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button_buy = InlineKeyboardButton(text='Смеситель', callback_data="product_buying")
button_buy2 = InlineKeyboardButton(text='Полотенцесушитель', callback_data="product_buying")
button_buy3 = InlineKeyboardButton(text='Ванна', callback_data="product_buying")
button_buy4 = InlineKeyboardButton(text='Унитаз', callback_data="product_buying")
kb_buy.insert(button_buy)
kb_buy.insert(button_buy2)
kb_buy.insert(button_buy3)
kb_buy.insert(button_buy4)


users = get_all_pictures()


s = 0
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Здравствуйте!", reply_markup=kb)


# Общая функция для запроса логина
async def ask_for_login(message: types.Message):
    await message.answer("Введите ваш логин:")
    await AuthStates.waiting_for_login.set()

# Общая функция для запроса пароля
async def ask_for_password(message: types.Message):
    await message.answer("Введите ваш пароль:")
    await AuthStates.waiting_for_password.set()

@dp.message_handler(lambda message: message.text == 'Вход')
async def process_login(message: types.Message):
    await ask_for_login(message)

# Добавляем обработчик для начала регистрации
@dp.message_handler(lambda message: message.text == 'Регистрация', state='*')
async def start_registration(message: types.Message, state: FSMContext):
    await state.update_data(is_registering=True)  # Устанавливаем флаг для регистрации
    await ask_for_login(message)

@dp.message_handler(state=AuthStates.waiting_for_login)
async def process_login_input(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await ask_for_password(message)

@dp.message_handler(state=AuthStates.waiting_for_password)
async def process_password_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data.get('login')
    password = message.text
    await state.update_data(password=password)

    # Проверяем, была ли инициирована регистрация
    if user_data.get('is_registering', False):  # Проверка на регистрацию
        # Запрашиваем повторный ввод пароля
        await message.answer("Пожалуйста, введите пароль ещё раз для подтверждения.")
        await AuthStates.waiting_for_password_confirmation.set()
    else:
        # Логика для входа
        if is_included(login, password):
            await message.answer("Вы успешно вошли!")
        else:
            await message.answer("Неверный логин или пароль. Попробуйте снова.")
            await state.finish()

@dp.message_handler(state=AuthStates.waiting_for_password_confirmation)
async def process_password_confirmation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    original_password = user_data.get('password')
    password_confirmation = message.text

    if password_confirmation == original_password:
        # Логика для проверки существования логина
        if not is_included(user_data.get('login'), user_data.get('password')):  # Проверяем, существует ли логин
            # Логика для регистрации
            # Например, сохранить пользователя в базе данных
            await message.answer("Вы успешно зарегистрированы!")
        else:
            await message.answer("Такой пользователь существует. Воспользуйтесь кнопкой Вход")
    else:
        await message.answer("Пароли не совпадают. Попробуйте снова.")

    # Завершаем состояние
    await state.finish()

# # Добавляем обработчик для начала регистрации
# @dp.message_handler(lambda message: message.text == 'Регистрация', state='*')
# async def start_registration(message: types.Message, state: FSMContext):
#     await state.update_data(is_registering=True)  # Устанавливаем флаг для регистрации
#     await ask_for_login(message)


# @dp.message_handler(text="Регистрация")
# async def main_menu(message):
#     await message.answer("Выберите опцию:", reply_markup=kb_in)


@dp.message_handler(text="Информация")
async def info(message):
    await message.answer("Меня зовут просто Помощник. Я помогу Вам в создании карточек для интернет-магазинов")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


#     для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(usnam=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(em=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(ag=message.text)
    data = await state.get_data()
    add_user(data['usnam'], data['em'], data['ag'])
    await message.answer("Регистрация прошла успешно!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
