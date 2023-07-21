from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
from create_bot import bot
from create_bot import dp
from keyboard import client_keyboard
from keyboard.inline_k import inline_keyboard, stat_inline, GPT_keyboard
from gpt_file import generate_response
import openai

openai.api_key = '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'
class MeInfo(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

class Maschine(StatesGroup):
    first = State()
    second = State()


async def start(message: types.Message):
    joined_file = open('user.txt', 'r')
    joined_users = set()
    for line in joined_file:
        joined_users.add(line.strip())
    if not str(message.chat.id) in joined_users:
        joined_file = open('user.txt', 'a')
        joined_file.write(str(message.chat.id) + '\n')
        joined_users.add(message.chat.id)
    await bot.send_message(message.chat.id, f'ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ',
                           reply_markup=client_keyboard, parse_mode='Markdown')


async def information(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите запрос')
    await Maschine.first.set()

async def gpt(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='asdf', reply_markup=GPT_keyboard)
    await state.finish()



@dp.callback_query_handler(text_contains='start_gpt')
async def start_gpt(call: types.CallbackQuery):
    tg_id = 'father'  # 1317283709

    # Отправляем статус, что бот печатает текст
    await bot.send_chat_action('father', "typing")
    # =========================================

    # Генерируем ответ с помощью chatgpt
    chatgpt_text_answer = generate_response(tg_id, 'father')

    # Отправляем ответ пользователю
    await call.message.reply(chatgpt_text_answer)

@dp.callback_query_handler(text_contains='cancel_gpt')
async def cancel_gpt(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы отменили выбор', parse_mode='Markdown')

async def stats(message: types.Message):
    await bot.send_message(message.chat.id, text='Хочешь посмотреть статистику бота?', reply_markup=stat_inline,
                           parse_mode='Markdown')


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Вот статистика бота*{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'У тебя нет админки\n Куда ты полез', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ты вернулся в главное меню. Жми опять кнопки', parse_mode='Markdown')


async def enter_meinfo(message: types.Message):
    if message.chat.id == config.admin:
        await message.answer('начинаем настройку. \n'  # Бот спрашивает ссылку
                             '№1 Введите линк на ваш профиль')
        await MeInfo.Q1.set()


async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)  # тут же он записывает наш ответ (наш линк)
    await message.answer('Линк сохранен.\n'
                         '№2 Введите текст.')
    await MeInfo.Q2.set()


async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)  # опять эе он записывает второй ответ

    await message.answer('Текст сохранен')

    data = await state.get_data()
    answer1 = data.get('answer1')  # тут он сует ответы в переменную, чтобы сохранить их в файле и вывести в след.сообщ
    answer2 = data.get('answer2')

    joinedFile = open('link.txt', 'w', encoding='utf-8')  # Вносим в файл encoding=utf-8, чтобы записывать смайлики
    joinedFile.write(str(answer1))
    joinedFile = open('text.txt', 'w', encoding='utf-8')  # Вносим в файл encoding=utf-8, чтобы записывать смайлики
    joinedFile.write(str(answer2))

    await message.answer(f'Ваша ссылка на профиль: {answer1}\n{answer2}')

    await state.finish()


async def developer(message: types.Message):
    link1 = open('link.txt', encoding='utf-8')  #
    link = link1.read()

    text_1 = open('text.txt', encoding='utf-8')  #
    text = text_1.read()
    await bot.send_message(message.chat.id, text=f'Создатель: {link}\n{text}', parse_mode='HTML')
    await bot.send_message(message.from_user.id, f'Разработчик')

async def photo(message: types.Message):
    await bot.send_photo(message.from_user.id, open('f4d2961b652880be432fb9580891ed62.jpg', 'rb'))


async def show_user(message: types.Message):
    await bot.send_message(message.from_user.id, 'Хочешь увидеть пользователя?', reply_markup=inline_keyboard)

@dp.callback_query_handler(text_contains='show_id')
async def show_id(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{call.message.chat.id}', parse_mode='Markdown')

@dp.callback_query_handler(text_contains='delete_id')
async def delete_id(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы отменили выбор', parse_mode='Markdown')



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(enter_meinfo, commands=['me'], state=None)
    dp.register_message_handler(answer_q1, state=MeInfo.Q1)
    dp.register_message_handler(answer_q2, state=MeInfo.Q2)
    dp.register_message_handler(information, commands=['Информация'], state=None)
    dp.register_message_handler(gpt, state=Maschine.first)
    dp.register_message_handler(stats, commands=['Статистика'])
    dp.register_message_handler(developer, commands=['Разработчик'])
    dp.register_message_handler(photo, commands=['Фото'])
    dp.register_message_handler(show_user, commands=['Покажи_пользователя'])
