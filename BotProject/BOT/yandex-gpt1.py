import requests

prompt = {
    "modelUri": "gpt://<ajej952ui67n2bkd5omp>/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты ассистент дроид, способный помочь в галактических приключениях."
        },
        {
            "role": "user",
            "text": "Привет, Дроид! Мне нужна твоя помощь, чтобы узнать больше о Силе. Как я могу научиться ее использовать?"
        },
        {
            "role": "assistant",
            "text": "Привет! Чтобы овладеть Силой, тебе нужно понять ее природу. Сила находится вокруг нас и соединяет всю галактику. Начнем с основ медитации."
        },
        {
            "role": "user",
            "text": "Хорошо, а как насчет строения светового меча? Это важная часть тренировки джедая. Как мне создать его?"
        }
    ]
}


url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key <AQVNw2xKDS92B4g_J0IC5rsvGJ6JQk6pAD5E76j_>"
}

response = requests.post(url, headers=headers, json=prompt)
result = response.text
print(result)


# aje3dh50qbrm0u43u9q2
# AQVNw2xKDS92B4g_J0IC5rsvGJ6JQk6pAD5E76j_