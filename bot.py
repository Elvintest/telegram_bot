import telebot
from datetime import datetime
from config import MainConfig, DB



bot = telebot.TeleBot(MainConfig.bot_key)
db = DB()






@bot.message_handler()
def routes(message):
    db.connect()
    # created connection
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    sql_check_precense = """select distinct user_id from user_states where user_id = %s;"""
    sql_check_status = """select state from user_states where user_id = %s"""
    # Checking the state of user out
    user_presence = db.query(sql_check_precense, (user_id,))
    if not user_presence:  # Проверка на пустой массив, массив, в котором нет данных, кроме других пустых массивов в Python False
        Introduction.start_message(user_id, user_name, db)
        db.close()
    else:
        user_state = db.query(sql_check_status, (user_id,))[0][0]  # Обращение к первому элементу кортежа массива
        if user_state == 'initial':
            WaitForEvent.ask_event(user_id, db)
            db.close()
        if user_state == 'wait_for_event':
            WaitForDate.ask_date(user_id, message, db)
            db.close()
        if user_state == 'wait_for_date':
            CompliteFillNotice.complite_form_user_notice(user_id, message, db)
            db.close()


class Introduction():
    @bot.message_handler(content_types=['text'])
    def start_message(user_id, user_name, db):
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard1.row('Задать напоминание')
        change_status_initial = """Insert into user_states (user_id,state) values (%s,'initial');"""
        db.execute(change_status_initial, (user_id,))
        bot.send_message(user_id,
                         f"Привет, {user_name}, очень рад, что ты обратился(ась) ко мне за помощью. Я могу "
                         f"напомнить тебе обо всем и в любое время!", reply_markup=keyboard1)


class WaitForEvent():
    def ask_event(user_id, db):
        change_status_wait_for_event = """update user_states set state = 'wait_for_event' where user_id = %s"""
        db.execute(change_status_wait_for_event, (user_id,))
        bot.send_message(user_id,
                         "Напиши, о чем тебе нужно напомнить:-)")


class WaitForDate():
    def ask_date(user_id, message, db):
        add_event = """insert into user_notices (user_id, body) values (%s,%s);"""
        body_even = message.text
        db.execute(add_event, (user_id, body_even))
        change_status_wait_for_date = """update user_states set state = 'wait_for_date' where user_id = %s;"""
        db.execute(change_status_wait_for_date, (user_id,))
        bot.send_message(user_id,
                         "Напиши, в какое время тебе напомнить о событии. Формат дд.мм.гггг чч:мм. Пример: 12.05.2020 12.30")


class CompliteFillNotice():
    keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard2.row('Начать диалог с ботом')

    def isInvalidDate(user_date):
        try:
            date = datetime.strptime(user_date, "%d.%m.%Y %H.%M")
        except:
            return False
        return date

    def complite_form_user_notice(user_id, message, db):
        user_date = message.text
        user_name = message.from_user.first_name
        complite_forming_event = """update  user_notices set date = %s where user_id = %s and date is %s;"""
        close_status = """delete from user_states where user_id = %s"""
        if CompliteFillNotice.isInvalidDate(user_date):
            db.execute(complite_forming_event, (CompliteFillNotice.isInvalidDate(user_date), user_id, None))
            db.execute(close_status, (user_id,))
            bot.send_message(user_id, f"Отлично, {user_name}, я все запомнил, напомню тебе об этом событии:-)",
                             reply_markup=CompliteFillNotice.keyboard2)
        else:
            bot.send_message(user_id,
                             "Напишите, пожалуйста корректную дату")


bot.polling(none_stop=True, interval=1)
