import telebot
import uuid  # случайное имя файла
import os
import speech_recognition as sr

from telebot import types

language = 'ru_RU'  # бот работает только на русском
TOKEN = '6287234764'  # от тг бота @BotFather
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)  # открываем аудиофайл, передаем в
            # r.recognize_google()
            return text
        except:
            print('Прости, не расслышал')
            return 'Прости, не расслышал'


@bot.message_handler(content_types=['start'])
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


@bot.message_handler(commands=['start'])
def start(message):
  markup = types.ReplyKeyboardMarkup()
  buttonA = types.KeyboardButton('A')         # пример изменения клавиатуры (с букв на выбор варианта)
  buttonB = types.KeyboardButton('B')
  buttonC = types.KeyboardButton('C')

  markup.row(buttonA, buttonB)
  markup.row(buttonC)
  bot.send_message(message.chat.id, 'Скоро голос персонажа будет готов!', reply_markup=markup)


bot.polling()
