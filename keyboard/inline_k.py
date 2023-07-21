from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = InlineKeyboardMarkup(row_width=1)
show_id = InlineKeyboardButton(text='Покажи id', callback_data='show_id')
delete_id = InlineKeyboardButton(text='Отменить выбор', callback_data='delete_id')
inline_keyboard.add(show_id).insert(delete_id)

stat_inline = InlineKeyboardMarkup(row_width=1)
stat_inline.add(InlineKeyboardButton('ДА', callback_data='join'))
stat_inline.add(InlineKeyboardButton('НЕТ', callback_data='cancel'))

GPT_keyboard = InlineKeyboardMarkup(row_width=2)
start_gpt = InlineKeyboardButton(text='Запустить ChatGPT', callback_data='start_gpt')
cancel_gpt = InlineKeyboardButton(text='Нинада', callback_data='cancel_gpt')
GPT_keyboard.add(start_gpt).insert(cancel_gpt)
