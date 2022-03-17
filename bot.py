import telebot
import schedule
import time
from threading import Thread

### Input data (token, participants, reset time)
bot = telebot.TeleBot('1373754699:AAE2ZCO8kiUQ7ZT3XQqWxzSBNsqkwFg82Os')
employees = ['Zorachki', 'lesja_hick', 'frolkin_test',]
reset_time = "22:10"    # in HH:MM(:SS) format

sleeping_list = employees[:]
woke_up_list = []

@bot.message_handler(content_types='text')
def get_text_messages(message):
    username = message.from_user.username
    ### Show the list of participants in a column 
    delimiter = '\n'
    awakened = delimiter.join(woke_up_list)
    sleeping = delimiter.join(sleeping_list)
    if message.text == '/status':
        if len(woke_up_list) == 0:
            bot.send_message(message.chat.id, "No one woke up")
        elif len(sleeping_list) == 0:
            bot.send_message(message.chat.id, f"Everyone woke up:\n{awakened}")
        else: bot.send_message(message.chat.id, f'Woke up:\n{awakened}\n\nStill sleeping:\n{sleeping}')
    elif message.text == '/help':
        bot.send_message(message.chat.id, '/help — help\n/status — awakened\n/count — number of awakened')
    elif message.text == '/count':
        current_count = len(woke_up_list)
        total_count = len(employees)
        bot.send_message(message.chat.id, f'Woke up {current_count} out of {total_count}')
    ### Adds a participant to the woke up list and removes from the sleepers
    if username in sleeping_list:
        woke_up_list.append(username)
        sleeping_list.remove(username)
   
def list_reset():
    """Transfers everyone from the woke up list to still sleeping"""
    for woke in woke_up_list:
        sleeping_list.append(woke)
    woke_up_list.clear()

def repeat():
    """Run resetting lists every day at the specified time"""
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
