import telebot
from telebot.types import Message
import psycopg2

"""
Telegram
"""
# запист в переменную токена полученного при регистрации бота
TOKEN = '842176662:AAELOFzSczA_c62AhehiITxI1iAzWxyvK54'
DB_NAME = 'dbn3od188bn1uk'
USER = 'xegtezjpppdscr'
PASSWORD = '0752bfc0afc8b03adf0147e874dee014f389636235f050f43f6488c68450e4e0'
HOST = 'ec2-176-34-184-174.eu-west-1.compute.amazonaws.com'

# создание экземпляра класса telebot
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def bot_commands(message: Message):
    bot.reply_to(message, 'Я предназначен для сохранения аудио файлов')
# разворачивоние функции с декоратором, слушающей сервер telegram
# установлен фильтр для приема аудиосообщений
@bot.message_handler(content_types=['voice'])
# синтакси message: Message предоставляет быстрый доступ к атрибутам и
# методам экземпляра класса message
def get_audio(message: Message):
    try:
        # создание экземпляра класса подклюсения с параметрами БД
        con = psycopg2.connect(
          database = DB_NAME,
          user = USER,
          password = PASSWORD,
          host = HOST,
          port="5432"
        )
        # получение атрибута file_id (понадобится для заполнения поля AUDIO)
        file_info = bot.get_file(message.voice.file_id)
        voice = str(file_info.file_path)
        # получение атрибута типа id типа User (понадобится для заполнения ID)
        id = message.from_user.id
        # создание объекта курсор, для работы с БД
        cur = con.cursor()
        # заполнение строки данными получеными ботом
        cur.execute(
        f"INSERT INTO audiosaver (ID, AUDIO) VALUES ({id},'{voice}')")
        # обновление БД
        con.commit()
        # закрытие соединения с БД
        con.close()
        # преобразование файла для его последующей загрузки
        downloaded_file = bot.download_file(file_info.file_path)
        # получение пути записи загруженного файла на диск
        path = str('C:\\Users\\Public\\' + file_info.file_path)
        # замена в пути символа '/' на символ '\' для ОС Windows
        #x = str('\\')
        path = path.replace('voice/','')
        # открытие файла в режиме записи в двоичном виде
        with open (path, 'wb') as new_file:
            # запись файла
            new_file.write(downloaded_file)
        # ответ бота в случае успешной загрузки
        bot.reply_to(message, f'Загрузил в БД сообщение {voice}')
    except Exception as erorr:
        print(erorr)
        # если загрузка необходима на ПК с ОС Linux
        if erorr == FileNotFoundError:
            try:
                path = str('/mnt/' + file_info.file_path)
                path = path.replace('voice/','')
                with open (path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, 'загрузил')
            except Exception as another_error:
                bot.reply_to(message, another_error)
        # ответ бота в случае неуспешной загрузки
        bot.reply_to(message, erorr)
# запросы серверера ботом с таймаутом
bot.polling(timeout=60)
