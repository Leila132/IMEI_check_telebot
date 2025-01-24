import telebot
from telebot.types import BotCommand
from database import get_db_connection, create_tables, check_user, check_user_auth_status, do_active_user
import requests
import json
from config import Config

bot = telebot.TeleBot(Config.TG_TOKEN)
commands = [
        BotCommand('start', 'Запустить бота'),
        BotCommand('help', 'Для чего нужен бот')
]
bot.set_my_commands(commands)

API_KEY = Config.API_KEY
url = Config.FULL_URL
headers = {
   'Authorization': 'Bearer ' + API_KEY,
   'Content-Type': 'application/json'
 }

conn = get_db_connection()
create_tables(conn)
conn.close()

@bot.message_handler(commands=['help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    conn = get_db_connection()
    is_user_in_db = check_user(conn, str(user_id))
    conn.close()
    if is_user_in_db:
        print("Пользователь с id: " + str(user_id) + " выполнил команду help.")
        bot.send_message(chat_id, "Привет! Я могу помочь тебе проверить imei через '" + Config.BASE_URL + "'. Напиши команду '/start' для начала")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    conn = get_db_connection()
    is_user_in_db = check_user(conn, str(user_id))
    auth_status = check_user_auth_status(conn, str(user_id))
    conn.close()
    if is_user_in_db:
        if auth_status == 0:
            print("Пользователь с id: " + str(user_id) + " выполнил команду start, ожидается авторизация.")
            bot.send_message(chat_id, "Отправь токен для авторизации!") 
        else:
            print("Пользователь с id: " + str(user_id) + " выполнил команду start, ожидается IMEI.")
            bot.send_message(chat_id, "Отправьте ваш IMEI, а я его проверю!") 


@bot.message_handler(func=lambda message: True)
def text(message):
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    conn = get_db_connection()
    is_user_in_db = check_user(conn, str(user_id))
    auth_status = check_user_auth_status(conn, str(user_id))
    conn.close()
    if is_user_in_db:
        if auth_status == 0:
                if text == API_KEY:
                    print("Пользователь с id: " + str(user_id) + " ввёл правильный ключ, заношу информацию о пройденной авторизации в бд.")
                    conn = get_db_connection()
                    do_active_user(conn, str(user_id))
                    conn.close()
                    print("Информация об авторизации пользователя с id: " + str(user_id) + " внесена.")
                    bot.send_message(chat_id, "Токен указан верно! Теперь вы можете отправлять ваш IMEI, а я его проверю!") 
                else:
                    print("Пользователь с id: " + str(user_id) + " ввёл неправильный ключ.")
                    bot.send_message(chat_id, "Токен неверный, попробуйте еще!") 
        else:
            print("Пользователь с id: " + str(user_id) + " сделал запрос.")    
            body = json.dumps({
                "deviceId": text, 
                "serviceId": Config.SERVICE_ID
            })
            response = requests.post(url, headers=headers, data=body)
            print("Ответ для пользователя с id: " + str(user_id) + " получен.") 
            formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
            bot.send_message(chat_id, formatted_json) 

bot.polling()