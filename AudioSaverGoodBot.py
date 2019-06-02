import telebot
from telebot.types import Message

# запист в переменную токена полученного при регистрации бота
TOKEN = '842176662:AAELOFzSczA_c62AhehiITxI1iAzWxyvK54'
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
        # получение атрибута file_id (понадобится для метода download_file)
        file_info = bot.get_file(message.voice.file_id)
        # преобразование файла для его последующей загрузки
        downloaded_file = bot.download_file(file_info.file_path)
        # получение пути записи загруженного файла на диск
        path = str('C:\\Users\\Public\\' + file_info.file_path)
        # замена в пути символа '/' на символ '\' для ОС Windows
        #x = str('\\')
        path = path.replace('voice/','')
        print (path)
        # открытие файла в режиме записи в двоичном виде
        with open (path, 'wb') as new_file:
            # запись файла
            new_file.write(downloaded_file)
        # ответ бота в случае успешной загрузки
        bot.reply_to(message, 'загрузил')
    except Exception as erorr:
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
