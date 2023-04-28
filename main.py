import os
import uuid
import soundfile
from gtts import gTTS
import speech_recognition as sr
import telebot
from telebot import types
import logging
from io import BytesIO
from aiogram import Dispatcher, executor, types


def telegram_bot(token):
    bot = telebot.TeleBot(token)
    r = sr.Recognizer()
    language = 'ru_RU'

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! Это Бот для озвучки персонажей! И не забываем про пасхалки =)")

    @bot.message_handler(content_types=["text"])
    def echo(message: types.Message):
        answer = checking_for_easter_eggs(message.text.lower())
        voice = converter_test_to_voice(message.text)
        bot.send_message(message.chat.id, answer)
        bot.send_voice(message.chat.id, voice)

    def converter_test_to_voice(text: str) -> BytesIO:
        bytes_file = BytesIO()
        audio = gTTS(text=text, lang='ru')
        audio.write_to_fp(bytes_file)
        bytes_file.seek(0)
        return bytes_file

    def checking_for_easter_eggs(text):
        easter_eggs = ["забудь заботы и держи трубой хвост!", "ты ходячая котострофа", "первое правило клуба",
                       "быть мертвецом не проблема", "28 ударов ножом",
                       "что вы выберете пиво или спасение души"]
        answer_for_easter_egg = ["Вот и весь секрет Живи сто лет Акуна матата!", "а ты ослостолоп",
                                 "не упоминать о бойцовском клубе", "быть забытым вот это гадко",
                                 "Ты действовал наверняка, да", "А какое пиво"]
        if text in easter_eggs:
            for line in easter_eggs:
                if text in line:
                    return answer_for_easter_egg[easter_eggs.index(line)]
        return text

    @bot.message_handler(content_types=["voice"])
    def voice_processing(message):
        filename = str(uuid.uuid4())
        with open('check.txt', mode='r', encoding='UTF-8') as file_txt:
            data = file_txt.readline()
            file_name_full = data + filename + ".ogg"
            file_name_full_converted = data + filename + ".wav"
        data, samplerate = soundfile.read(file_name_full)
        soundfile.write(file_name_full_converted, data, samplerate)
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i " + file_name_full + "  " + file_name_full_converted)
        text = recognise(file_name_full_converted)
        bot.reply_to(message, text)
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    def recognise(filename):
        with sr.AudioFile(filename) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language=language)
                print('Converting audio transcripts into text ...')
                print(text)
                return text
            except Exception as ex:
                print('Sorry.. run again...')
                print(ex)
                return "Sorry.. run again..."

    @bot.message_handler(content_types=['photo'])
    def get_user_photo(message):
        bot.send_message(message.chat.id, 'Вау, классное фото!')

    @bot.message_handler(commands=['help'])
    def website(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        start = types.KeyboardButton('Start')
        # button_Pumba = types.KeyboardButton('Пумба')  # из "Король лев"
        # button_Osel = types.KeyboardButton('Осёл')  # из шрека
        # button_Tayler = types.KeyboardButton('Тайлер Дердан')  # из "Бойцовский клуб"
        # button_Vurhiz = types.KeyboardButton('Джейсон Вурхиз')  # из "пятница 13"
        # button_Android = types.KeyboardButton('Андроид')  # из игры "Detroit: Become Human"
        # button_Gomer = types.KeyboardButton('Гомер Симпсон')
        markup.add(start)
        # markup.row(button_Pumba)
        # markup.row(button_Osel)
        # markup.row(button_Tayler)
        # markup.row(button_Vurhiz)
        # markup.row(button_Gomer)
        # markup.row(button_Android)
        bot.send_message(message.chat.id, 'Скоро голос персонажа будет готов!', reply_markup=markup)

    bot.polling()


if __name__ == '__main__':
    with open('token.txt', 'r', encoding='UTF-8') as file:
        data = file.readline()
        telegram_bot(data)
