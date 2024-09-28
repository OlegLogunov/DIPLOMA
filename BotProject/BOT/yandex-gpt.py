import requests

   # Замените 'YOUR_API_KEY' на ваш реальный API-ключ
API_KEY = 'AQVN1drN9NN2eKHXPELkO3dE9nVbixtPK22IB2R-'
API_URL = 'https://api.yandex.cloud.ai/gpt/v1/complete'  # Убедитесь, что это правильный URL

headers = {
    'Authorization': f'Api-Key {API_KEY}',
    'Content-Type': 'application/json',
}

data = {
    'model': 'gpt-3',  # Убедитесь, что используете правильную модель
    'prompt': 'Ваш текст запроса',
    'max_tokens': 100,
}

try:
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()  # Вызывает исключение для кода состояния 4xx/5xx
    result = response.json()
    print(result['choices'][0]['text'])  # Извлечение текста ответа
except requests.exceptions.RequestException as e:
    print(f'Ошибка запроса: {e}')


# ajelrb6v9krmf2gtef22
# AQVN1drN9NN2eKHXPELkO3dE9nVbixtPK22IB2R-