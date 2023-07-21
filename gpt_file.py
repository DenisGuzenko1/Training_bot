import aiogram
import openai
users_chat_history = {}

def init_user_chat(tg_id):
    # Для конкретного пользователя мы задаем настройку chatGPT
    users_chat_history[tg_id] = [
        {
            "role": "system",
            "content": "Ты помощник, который отвечает правильно и с подробным пояснением ответа.",
        }
    ]


# Создаем функцию для генерации ответа с помощью chatgpt
def generate_response(tg_id, message):
    # tg_id - идентификатор пользователя
    # message - его сообщение

    # Если еще нет истории чата для `tg_id`, инициализируем чат
    if tg_id not in users_chat_history:
        init_user_chat(tg_id)  # Вызов функции для инициализации чата

    # После этого у нас уже есть настройка чата и первый запрос к chatGPT

    # Добавляем в историю чата новый запрос пользователя
    users_chat_history[tg_id].append(
        {
            "role": "user",
            "content": message,
        }
    )

    # Делаем запрос в ChatGPT и получаем результат
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=users_chat_history[tg_id],  # Отправляем всю историю чата
        temperature=0.7,
    )

    # Ответ от ChatGPT (текстовый)
    chat_gpt_answer = response["choices"][-1]["message"]["content"]

    # Добавляем ответ от ChatGPT в историю чата
    users_chat_history[tg_id].append(
        {
            "role": "assistant",  # Роль другая
            "content": chat_gpt_answer,
        }
    )
    return chat_gpt_answer