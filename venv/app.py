from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

import random
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('bot_token'))
dp = Dispatcher()

#kb_bilder=ReplyKeyboardBuilder()
ReplyKeyboardRemove()
web_app_button=KeyboardButton(text='open web', web_app=WebAppInfo(url='https://stepik.org/users/458255021/certificates'))
web_app_keyboad=ReplyKeyboardMarkup(keyboard=[[web_app_button]], resize_keyboard=True)


COUNT_GAME_ALL = 5
user = {'in_game':False, 
        'select_number':None,
        'count_game': None,
        'total_game':0,
        'wins_of_user_game':0}

def get_random_number()->int:
    return random.randint(1,101)

def get_input_nuber(message: Message):
    if message.text and message.text.isdigit() and 0<int(message.text)<101:
        return int(message.text)

@dp.message(CommandStart())
async def ferst_start_command(message: Message):
    await message.answer(
        'Тут можно сыграть с ботом в игру УГАДАЙКА число \n'
        'список доступных команд: /help и /cansel')
    
@dp.message(Command(commands='webapp'))
async def web_app_command(message: Message):
    await message.answer(text='test web app', reply_markup=web_app_keyboad)

@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(
        f'инструкция: необходимо сыграть с роботом, в игру УГАДАЙКА число\n'
        f'Робот загадает число от 1 до 100, необходимо угдать с {user["count_game"]} попыток\n'
    )  # f'статистика игры: \nвыиграно {user_gamer["wins_of_user_game"]} и проиграно{user_gamer["total_game"] - user_gamer["wins_of_user_game"]}'

@dp.message(Command(commands='stat'))
async def stats_command(message: Message):
    await message.answer(
        f'пошла жара, пора играть\n'
        f'стaтистика: {user["total_game"]}, выигранных: {user["wins_of_user_game"]}'
    )

@dp.message(Command(commands='cansel'))
async def cansel_command(message: Message):
    if user['in_game']:
        user['in_game']=False
        await message.answer('изи, легкая победа - минусу балл, сыграть еще - /start')
    else:
        await message.answer(
            'так мы и так не играем\n'
            'доступные команды: - /stat, /help, /cansel')                         

@dp.message(F.text.lower().in_(['да', "ок", "конечно", "давай"]))
async def game_on_command(message: Message):
    if not user['in_game']:
        user['in_game']=True
        user['select_number']=get_random_number()
        user['count_game']=COUNT_GAME_ALL
        await message.answer('бот загадал число от 1 до 100, попробуй угадать')
    else:
        await message.answer('пока играем, есть кнопка стистики /stat или /cansel')

@dp.message(get_input_nuber)
async def process_game_command(message: Message):
    if user['in_game']:
        if int(message.text) == user['select_number']:
            user['in_game']=False
            user['total_game']+=1
            user['wins_of_user_game']+=1
            await message.answer(f'Крассавчег, угадал с {user["count_game"]} попытки')
        elif int(message.text) > user['select_number']:
            user['count_game']-=1
            await message.answer('загаданное ботом число меньше')
        elif int(message.text) < user['select_number']:
            user['count_game']-=1
            await message.answer('загаданное ботом число больше')
        if user['count_game']==0:
            user['in_game']=False
            user['total_game']+=1
            await message.answer(
                f'Все попытки исчерпаны, вы проиграли\n'
                f'загаданное ботом число - {user["select_number"]}')
    else:
        await message.answer('Мы еще не играем, доступные команды: - /stat, /help, /cansel')

@dp.message()
async def other_command(message: Message):
    if user['in_game']:
        await message.answer(
            'Мы же еще играем, бот ждет число от 1 до 100, \n'
            'доступные команды: - /stat, /help, /cansel \n'
            'Внимание: введенные данные состовляют абракадабру но не цифры')
    else:
        await message.answer(
            'больше бот пока ничего не умеет '
            'введенные данные состовляют абракадабру но не цифры '
            'доступные команды: - /stat, /help, /cansel')

if __name__=='__main__':
    dp.run_polling(bot)