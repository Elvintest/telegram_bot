import time
from config import MainConfig, DB
from datetime import datetime
import telebot
db = DB()
db.connect()
bot = telebot.TeleBot(MainConfig.bot_key)

check_ready_notifications = """select user_id, body from user_notices where date < %s;""" # Выбираем нотификации, срок которых меньше текущей даты
clean_ready_notifications = """delete from user_notices where body = %s;""" # Удаляем нотификации, которые отправили


response = db.query(check_ready_notifications,(datetime.now(),))

if response: # если в базе есть нотификашки
    amount_notifications = 0
    for i in response:
        bot.send_message(i[0],f'Привет, напоминаю о событии: {i[1]}') # оповещаем пользователей
        amount_notifications +=1
    for i in response:
        db.execute(clean_ready_notifications,(i[1],))
    print(f'sending {amount_notifications} notifications has successfully complited')
else:
    print(f'new notifications for {datetime.now()} were not found')
