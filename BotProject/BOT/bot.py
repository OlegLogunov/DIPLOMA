import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor
from PIL import Image
import requests
from io import BytesIO

API_TOKEN = '7594342351:AAHFSdUfGDK3F4VTsItara30erCvanOhTg4'

# Настройка логирования 
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера 
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



# from deeppavlov import build_model, configs
#
#
# def describe_image(image_path):
#     # Загружаем модель для описания изображений
#     model = build_model(configs.img_captioning.captioning, download=True)
#
#     # Предполагаем, что image_path - это путь к изображению
#     # В зависимости от модели может потребоваться преобразование изображения в нужный формат
#     description = model([image_path])
#
#     return description[0]  # Возвращаем описание первого изображения
#
#
# # Пример использования
# image_path = 'C:\\Users\\1\\PycharmProjects\\BotProject\\BOT\\162739.jpg'
# description = describe_image(image_path)
# print(description)



# import openai
#
#
# def describe_image(image_path):
#     # Открываем изображение
#     with open(image_path, "rb") as image_file:
#         image_data = image_file.read()
#
#     # Отправляем запрос к OpenAI API
#     response = openai.Image.create(
#         file=image_data,
#         purpose="caption"
#     )
#
#     # Извлекаем текстовое описание из ответа
#     description = response['data'][0]['text']
#
#     return description


#
# # Пример использования
# image_description = describe_image("path_to_your_image.jpg")
# print(image_description)

# def describe_image(image):    # Здесь вы можете использовать любую модель для описания изображения.
#     return "Красивая картинка"
#
# @dp.message_handler(content_types=['photo'])
# async def handle_photo(message: types.Message):
#     # Получаем файл изображения
#     photo = message.photo[-1]  # Берем самое большое изображение
#     file_id = photo.file_id
#     file_info = await bot.get_file(file_id)
#
#     # Загружаем изображение
#     downloaded_file = await bot.download_file(file_info.file_path)
#
#     # Открываем изображение с помощью Pillow
#     image = Image.open(BytesIO(downloaded_file.getvalue()))
#
#     # Генерируем описание изображения
#     description = describe_image(image)
#
#     # Отправляем описание обратно пользователю
#     await message.reply(description)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)


from transformers import CLIPProcessor, CLIPModel
# from PIL import Image
# import requests


def describe_image(image_path):
    # Загрузка модели и процессора
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

    # Загрузка изображения
    if image_path.startswith('http'):
        image = Image.open(requests.get(image_path, stream=True).raw)
    else:
        image = Image.open(image_path)

    # Подготовка данных для модели
    inputs = processor(text=["a photo of a cat", "a photo of a dog", "a photo of a car"], images=image,
                       return_tensors="pt", padding=True)

    # Получение предсказаний
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # Логиты для изображений
    probs = logits_per_image.softmax(dim=1)  # Вероятности

    # Получение описания с наибольшей вероятностью
    description_index = probs.argmax().item()
    descriptions = ["a photo of a cat", "a photo of a dog", "a photo of a car"]

    return descriptions[description_index]


# Пример использования
image_url = "https://www.vodoparad.ru/upload/webp/big14b91z2cz3ymfz5huoof9t4vh3nruutvpkim363895AQ1080CR.webp"
print(describe_image(image_url))