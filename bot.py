import telebot
import schedule
import time
from threading import Thread

### Вводные данные (токен, участники, время сброса)
bot = telebot.TeleBot('1373754699:AAE2ZCO8kiUQ7ZT3XQqWxzSBNsqkwFg82Os')
employees = ['Zorachki', 'lesja_hick', 'frolkin_test',]
reset_time = "22:10"    # в формате HH:MM(:SS)

sleeping_list = employees[:]
woke_up_list = []

@bot.message_handler(content_types='text')
def get_text_messages(message):
    username = message.from_user.username
    ### Выводит список участников в столбик
    delimiter = '\n'
    awakened = delimiter.join(woke_up_list)
    sleeping = delimiter.join(sleeping_list)
    if message.text == '/status':
        if len(woke_up_list) == 0:
            bot.send_message(message.chat.id, "Все ещё спят")
        elif len(sleeping_list) == 0:
            bot.send_message(message.chat.id, f"Все проснулись:\n{awakened}")
        else: bot.send_message(message.chat.id, f'Проснулись:\n{awakened}\n\nЕщё спят:\n{sleeping}')
    elif message.text == '/help':
        bot.send_message(message.chat.id, '/help — помощь\n/status — проснувшиеся\n/count — количество проснувшихся')
    elif message.text == '/count':
        current_count = len(woke_up_list)
        total_count = len(employees)
        bot.send_message(message.chat.id, f'Проснулось {current_count} из {total_count}')
    if message.text == "loh":
        bot.send_message(message.chat.id, "Лох")
    ### Добавляет человека в список проснувшихся и удаляет из спящих
    if username in sleeping_list:
        woke_up_list.append(username)
        sleeping_list.remove(username)
   
def list_reset():
    """Переносит всех из списка проснувшихся в ещё спящих"""
    for woke in woke_up_list:
        sleeping_list.append(woke)
    woke_up_list.clear()

def repeat():
    """Запускает сброс списков каждый день в заданное время"""
    schedule.every().day.at(reset_time).do(list_reset)
    while True:
        schedule.run_pending()
        time.sleep(1)

def bot_working():
    bot.polling(none_stop=True, interval=0)

thread1 = Thread(target=bot_working)
thread2 = Thread(target=repeat)

thread1.start()
thread2.start()
thread1.join()
thread2.join()