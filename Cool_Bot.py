import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from j import google_image_downloader
from test2 import download_audio
from data import token #импорт токена

bot = Bot(token=f"{token}")

dp = Dispatcher(bot)

button1 = KeyboardButton("Отправить изображение")
button2 = KeyboardButton("Отправить аудиофайл")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2)

user_requests = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Отправить изображение")
async def ask_for_image_query(message: types.Message):
    user_requests[message.from_user.id] = "awaiting_query_img"  
    await message.reply("Какое изображение вы хотите получить? Напишите запрос.")

@dp.message_handler(lambda message: message.text == "Отправить аудиофайл")
async def send_help(message: types.Message):
    user_requests[message.from_user.id] = "awaiting_query_mp3"  
    await message.reply("Какой аудиофайл вы хотите получить? Напишите запрос.")

@dp.message_handler()
async def handle_query(message: types.Message):
    user_id = message.from_user.id
    
    if user_requests.get(user_id) == "awaiting_query_img":
        query = message.text
        user_requests[user_id] = None  

        google_image_downloader(query)
        photo = InputFile('img/000001.jpg')  
        await message.answer_photo(photo=photo,
                                caption='Вот ваше изображение!')
        
    elif user_requests.get(user_id) == "awaiting_query_mp3":
        query = message.text
        user_requests[user_id] = None

        download_audio(query)
        with open('audio/test.mp3', 'rb') as audio:
          await message.answer_audio(audio)
        

executor.start_polling(dp, skip_updates=True)
        