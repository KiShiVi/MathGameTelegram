from random import randrange
from telebot import types
from enum import Enum
import telebot

TOKEN = '2143235398:AAG3fZqyrcJt8kETVgRGI1gSpFAsVQrIJl8'

bot = telebot.TeleBot(TOKEN)

startedGamesID = set()


class Status(Enum):
    MAIN_MENU = 0
    CREATE = 1
    JOIN = 2


class User:
    def __init__(self, chat_id, status=Status.MAIN_MENU, game_id=0):
        self.chat_id = chat_id
        self.status = status
        self.game_id = game_id


userSet = set()


def getUserStatus(chat_id):
    for user in userSet:
        if user[0] == chat_id:
            return user[1].status
    raise Exception("User not found")


def updateUser(chat_id, status=Status.MAIN_MENU, game_id=0):
    userSet.add((chat_id, User(chat_id, status, game_id)))


@bot.message_handler(commands=['start'])
def handle_start(message):
    updateUser(message.chat.id, status=Status.MAIN_MENU)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("/create"))
    markup.row(types.KeyboardButton("/join"))
    bot.send_message(message.chat.id, 'Welcome!\nFind yourself an opponent!', reply_markup=markup)


@bot.message_handler(commands=['create'])
def handle_id_generator(message):
    gameID = randrange(1000, 9999)
    while gameID in startedGamesID:
        gameID = randrange(1000, 9999)

    startedGamesID.add(gameID)

    updateUser(message.chat.id, status=Status.CREATE, game_id=gameID)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/cancel"))
    bot.send_message(message.chat.id, 'Your ID: {}, show it to your friend'.format(gameID), reply_markup=markup)


@bot.message_handler(commands=['join'])
def handle_join(message):
    updateUser(message.chat.id, status=Status.JOIN)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("/cancel"))
    bot.send_message(message.chat.id, 'Enter ID of friend: ', reply_markup=markup)

    @bot.message_handler()
    def nextWord(message2):
        if message2.text not in startedGamesID:
            bot.send_message(message2.chat.id, 'This game is not found')
        else:
            ###
            bot.send_message(message2.chat.id, 'Game found!')


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    if (getUserStatus(message.chat.id) == Status.CREATE or
            getUserStatus(message.chat.id) == Status.JOIN):
        updateUser(message.chat.id, status=Status.MAIN_MENU)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("/create"))
        markup.row(types.KeyboardButton("/join"))
        bot.send_message(message.chat.id, 'Welcome!\nFind yourself an opponent!', reply_markup=markup)


bot.infinity_polling()

'''
This is buttons

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Кнопка")
markup.row(item1, item1, item1)
markup.row(item1, item1, item1)
markup.row(item1, item1, item1)
bot.send_message(message.chat.id, 'Welcome', reply_markup=markup)
'''
