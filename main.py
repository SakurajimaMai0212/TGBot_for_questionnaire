import telebot
import config
from telebot import types
import sqlite3

bot = telebot.TeleBot(config.TOKEN)

connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    answer = bot.send_message(message.from_user.id, text=config.start_and_name_message)

    bot.register_next_step_handler(answer, names)

@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    if call.data:
        global city
        city = call.data

        config.ret = config.ret + city + '\n'

        number = bot.send_message(call.from_user.id, text=config.number_message)

        bot.register_next_step_handler(number, num)

def names(message):
    global name
    name = message.text

    config.ret = config.ret + name + '\n'

    markup = types.InlineKeyboardMarkup()

    for i in range(len(config.mas_cities)):
        markup.add(types.InlineKeyboardButton(text=config.mas_cities[i], callback_data=config.mas_cities[i]))

    bot.send_message(message.from_user.id, text=config.city_message, reply_markup=markup)

def num(message):
    global num
    num = message.text

    cursor.execute('INSERT INTO Users (name, city, number) VALUES (?, ?, ?)', (name, city, num))
    connection.commit()

    config.ret = config.ret + num

    bot.send_message(config.mas[city], text=config.ret)
    bot.send_message(config.admin, text=config.ret)
    bot.send_message(0213124, text=config.ret)

bot.polling(non_stop=True)
