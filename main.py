import os
from dotenv import load_dotenv
import telebot
from telebot import types
from time import sleep
load_dotenv()
telegramtoken = os.environ["TELEGRAMTOKEN"]
telegramid = os.environ["TELEGRAMID"]
bot = telebot.TeleBot(telegramtoken)

class Account:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash

    def show_account(self):
        return f"На вашем счету {self.name} находится {self.cash} рублей"

    def get_decrease(self, decrease):
        self.cash -= decrease
        return f"На Вашем счету {self.name} теперь {self.cash} рублей"

    def get_increase(self, increase):
        self.cash += increase
        return f"На Вашем счету {self.name} теперь {self.cash} рублей"

accs = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    if len(accs) != 0:
        btn1 = types.InlineKeyboardButton(text="Создать счёт", callback_data="create_account")
        btn2 = types.InlineKeyboardButton(text="Удалить счёт", callback_data="del_account")
        btn3 = types.InlineKeyboardButton(text="Выбор счёта", callback_data="accounts")
        markup.row(btn1, btn2)
        markup.row(btn3)
    else:
        btn2 = types.InlineKeyboardButton(text="Создать счёт", callback_data="create_account")
        markup.row(btn2)
    bot.send_message(telegramid, text="Какое действие хотите совершить?", reply_markup=markup)
    sleep(1)

@bot.callback_query_handler(func=lambda call: call.data.startswith('start'))
def start(message):
    markup = types.InlineKeyboardMarkup()
    if len(accs) != 0:
        btn1 = types.InlineKeyboardButton(text="Создать счёт", callback_data="create_account")
        btn2 = types.InlineKeyboardButton(text="Удалить счёт", callback_data="del_account")
        btn3 = types.InlineKeyboardButton(text="Выбор счёта", callback_data="accounts")
        markup.row(btn1, btn2)
        markup.row(btn3)
    else:
        btn2 = types.InlineKeyboardButton(text="Создать счёт", callback_data="create_account")
        markup.row(btn2)
    bot.send_message(telegramid, text="Какое действие хотите совершить?", reply_markup=markup)
    sleep(1)

@bot.callback_query_handler(func=lambda call: call.data.startswith('create_account'))
def get_react(message):
    markup = types.InlineKeyboardMarkup()
    message = bot.send_message(telegramid, text="Как вы хотите назвать ваш счёт?", reply_markup=markup)
    bot.register_next_step_handler(message, create_account1)

def create_account1(message):
    markup = types.InlineKeyboardMarkup()
    global name
    name = message.text
    message = bot.send_message(telegramid, text="Сколько денег у вас на счету?", reply_markup=markup)
    bot.register_next_step_handler(message, create_account2)

def create_account2(message):
    global name
    accs.append(Account(name, int(message.text)))
    markup = types.InlineKeyboardMarkup()
    bot.send_message(telegramid, text="Счёт создан", reply_markup=markup)
    sleep(1)
    start(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('del_account'))
def deletable_account(message):
    markup = types.InlineKeyboardMarkup()
    for acc in accs:
        markup.add(types.InlineKeyboardButton(text=acc.name, callback_data=f"deliting_account {acc.name}"))
    bot.send_message(telegramid, text="Какой счёт вы хотите удалить?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('deliting_account'))
def del_acc1(message):
    markup = types.InlineKeyboardMarkup()
    deliting_acc = message.data.split(" ")[1]
    btn1 = types.InlineKeyboardButton(text="Да", callback_data=f"current_del_acc {deliting_acc}")
    btn2 = types.InlineKeyboardButton(text="Нет", callback_data='start')
    markup.row(btn1, btn2)
    bot.send_message(telegramid, text="Вы уверены, что хотите удалить счёт?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('current_del_acc'))
def del_acc2(message):
    deleted_acc = message.data.split(" ")[1]
    for acc in accs:
        if acc.name == deleted_acc:
            accs.remove(acc)
    bot.send_message(telegramid, text=f"Счёт {deleted_acc} удалён")
    sleep(1)
    start(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('account'))
def account1(message):
    markup = types.InlineKeyboardMarkup()
    for acc in accs:
        markup.add(types.InlineKeyboardButton(text=acc.name, callback_data=f"use_acc {acc.name}"))
    markup.add(types.InlineKeyboardButton(text="Назад", callback_data="start"))
    bot.send_message(telegramid, text="Счета на выбор", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('use_acc'))
def account2(message):
    global using_acc
    using_acc = message.data.split(" ")[1]
    markup = types.InlineKeyboardMarkup()
    for acc in accs:
        if using_acc == acc.name:
            using_acc = acc
    btn1 = types.InlineKeyboardButton(text="Добавить расход", callback_data="act_account")
    btn2 = types.InlineKeyboardButton(text="Добавить доход", callback_data="acc_act")
    btn3 = types.InlineKeyboardButton(text="Назад", callback_data="account")
    markup.row(btn1, btn2)
    markup.row(btn3)
    sleep(1)
    bot.send_message(telegramid, text=f"{using_acc.show_account()}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('act_account'))
def account_acts1(message):
    markup = types.InlineKeyboardMarkup()
    message = bot.send_message(telegramid, text="Сколько было потрачено?", reply_markup=markup)
    bot.register_next_step_handler(message, account_decrease)

@bot.callback_query_handler(func=lambda call: call.data.startswith('acc_act'))
def account_acts2(message):
    markup = types.InlineKeyboardMarkup()
    message = bot.send_message(telegramid, text="Сколько было получено?", reply_markup=markup)
    bot.register_next_step_handler(message, account_increase)

def account_decrease(message):
    markup = types.InlineKeyboardMarkup()
    decrease = int(message.text)
    bot.send_message(telegramid, text=f"{using_acc.get_decrease(decrease)}", reply_markup=markup)
    sleep(1)
    start(message)

def account_increase(message):
    markup = types.InlineKeyboardMarkup()
    increase = int(message.text)
    bot.send_message(telegramid, text=f"{using_acc.get_increase(increase)}", reply_markup=markup)
    sleep(1)
    start(message)

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
