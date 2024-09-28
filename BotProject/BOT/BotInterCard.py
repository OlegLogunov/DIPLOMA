import sys

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
button4 = KeyboardButton(text='Завершение работы')
kb.insert(button)
kb.insert(button2)
kb.insert(button3)
kb.insert(button4)

kb_p = InlineKeyboardMarkup(resize_keyboard=True)
button_p = KeyboardButton(text='Загрузите изображение', callback_data="picture")
button2_p = KeyboardButton(text='Завершение работы', callback_data="exit")
kb_p.insert(button_p)
kb_p.insert(button2_p)

kb_c = InlineKeyboardMarkup(resize_keyboard=True)
button_c = KeyboardButton(text='Продолжить', callback_data="picture")
button2_c = KeyboardButton(text='Завершить', callback_data="exit")
kb_c.insert(button_c)
kb_c.insert(button2_c)

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

# Общая функция для завершения работы
async def send_goodbye(message: types.Message):
    await message.answer("Спасибо за использование нашего приложения. До свидания!")
    await bot.close()  # Закрывает соединение с Telegram API
    sys.exit()  # Завершает выполнение скрипта

# Общая функция для завершения работы
async def image_proc(message: types.Message):
    await message.answer("Запуск процедуры обработки изображения и формирования описания с помощью ИИ")


@dp.message_handler(text="Информация")
async def info(message):
    # await message.answer("Меня зовут просто Помощник. Я помогу Вам в создании карточек для интернет-магазинов")
    await message.answer("Выберите опцию: ", reply_markup=kb_p)

@dp.callback_query_handler(text="exit")
async def info_call(call):
    await send_goodbye(call)

@dp.callback_query_handler(text="picture")
async def work_pict(call):
    await image_proc(call)
    await call.message.answer("Дальнейшие действия: ", reply_markup=kb_c)

@dp.message_handler(text="Завершение работы")
async def ex_info(message):
    await send_goodbye(message)


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
            await message.answer(f"Добро пожаловать, {user_data.get('login')}")
            await message.answer("Дальнейшие действия: ", reply_markup=kb_p)
        else:
            await message.answer("Неверный логин или пароль. Попробуйте снова.")
            await state.finish()


@dp.message_handler(state=AuthStates.waiting_for_password_confirmation)
async def process_password_confirmation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    original_password = user_data.get('password')
    password_confirmation = message.text

    if password_confirmation == original_password:
        # Логика для проверки существования логина и пароля
        if not is_included(user_data.get('login'), user_data.get('password')):  # Проверяем, существует ли логин и пароль
            await message.answer("Вы успешно зарегистрированы!")
            add_user(user_data.get('login'), user_data.get('password'))
            await message.answer(f"Добро пожаловать, {user_data.get('login')}")
            await message.answer("Дальнейшие действия: ", reply_markup=kb_p)
        else:
            await message.answer("Такой пользователь существует. Воспользуйтесь кнопкой Вход")
    else:
        await message.answer("Пароли не совпадают. Попробуйте снова.")

    # Завершаем состояние
    await state.finish()


# @dp.message_handler(text="Добро пожаловать")
# async def work(message):
#     await message.answer("", reply_markup=kb_p)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
