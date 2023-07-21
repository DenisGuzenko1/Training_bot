from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

info = KeyboardButton('/Информация')
stats = KeyboardButton('/Статистика')
dev = KeyboardButton('/Разработчик')
user_show = KeyboardButton('/Покажи_пользователя')
photo = KeyboardButton('/Фото')

client_keyboard.add(info).insert(stats).add(dev).insert(user_show).add(photo)
