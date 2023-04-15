import dp as dp
import telebot
import uuid  # случайное имя файла
import os
import speech_recognition as sr
import requests
import subprocess
import datetime
from django.conf import settings


from telebot import types


language = 'ru_RU'  # бот работает только на русском
TOKEN = settings.MY_API_KEY  # от тг бота @BotFather
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)  # открываем аудиофайл, передаем в
            # r.recognize_google()
            return text
        except Exception:
            print('Прости, не расслышал')
            return 'Прости, не расслышал'


@bot.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это Бот для озвучки персонажей! И не забываем про пасхалки =). Для продолжения выберите 'help'")


def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "./voice/" + filename + ".ogg"
    file_name_full_converted = "./ready/" + filename + ".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i " + file_name_full + "  " + file_name_full_converted)
    text = recognise(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

tts = TTS()


@dp.message_handler(content_types=["help"])
async def cmd_text(message: types.Message):
    await message.reply("Текст получен")
    out_filename = tts.text_to_ogg(message.text)
    path = Path("", out_filename)                      # отправка гс
    voice = InputFile(path)
    await bot.send_voice(message.from_user.id, voice,
                         caption="Ответ от бота")
    os.remove(out_filename)                            # Удаление временного файла


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button_Pumba = types.KeyboardButton('Пумба') # из "Король лев"
    button_Osel = types.KeyboardButton('Осёл') # из шрека
    button_Tayler = types.KeyboardButton('Тайлер Дердан') # из "Бойцовский клуб"
    button_Vurhiz = types.KeyboardButton('Джейсон Вурхиз') # из "пятница 13"
    button_Android = types.KeyboardButton('Андроид') # из игры "Detroit: Become Human"
    button_Gomer = types.KeyboardButton('Гомер Симпсон')

    markup.row(button_Pumba)
    markup.row(button_Osel)
    markup.row(button_Tayler)
    markup.row(button_Vurhiz)
    markup.row(button_Vurhiz)
    markup.row(button_Gomer)
    markup.row(button_Android)
    bot.send_message(message.chat.id, 'Скоро голос персонажа будет готов!', reply_markup=markup)


if message.text.lower() == "Забудь заботы и держи трубой хвост":
    await bot.send_message(message.chat.id, "Вот и весь секрет живи сто лет акуна матата!")
if message.text.lower() == "Ты ходячая котострофа":
    await bot.send_message(message.chat.id, "а ты ослостолоп")
if message.text.lower() == "первое правило клуба":
    await bot.send_message(message.chat.id, "не упоминать о бойцовском клубе")
if message.text.lower() == "быть мертвецом не проблема":
    await bot.send_message(message.chat.id, "быть забытым вот это гадко")
if message.text.lower() ==  "Двадцать восемь ударов ножом":
    await bot.send_message(message.chat.id, "Ты действовал наверняка да")
if message.text.lower() == "Что вы выберете пиво или спасение души":
    await bot.send_message(message.chat.id, "А какое пиво")
''' Пасхалки:
Пумба - "Забудь заботы И держи трубой хвост!" -> "Вот и весь секрет Живи сто лет Акуна матата!"
Осёл - "Ты ходячая котострофа" —> "а ты ослостолоп"
Тайлер - "первое правило клуба" -> "не упоминать о бойцовском клубе"
Джейсон - "быть мертвецом не проблема" -> "быть забытым вот это гадко"
Андроид - "28 ударов ножом" -> "Ты действовал наверняка, да" (из игры "Detroit: Become Human")
Гомер - "Что вы выберете пиво или спасение души" -> "А какое пиво'''

bot.polling()
