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


userSet = {}


def getUser(chat_id):
    if userSet.get(chat_id) is not None:
        return userSet[chat_id]
    raise Exception("User not found")


def getOpponent(game_id, not_chat_id):
    for key in userSet.keys():
        if userSet[key].game_id == game_id and \
                key != not_chat_id:
            return userSet[key]
    raise Exception("Opponent not found")


def updateUser(chat_id, status=Status.MAIN_MENU, game_id=0):
    userSet.update({chat_id: User(chat_id, status, str(game_id))})


@bot.message_handler(commands=['start'])
def handle_start(message):
    print(str(message.chat.id) + ' ' + message.text)

    updateUser(message.chat.id, status=Status.MAIN_MENU)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("/create"))
    markup.row(types.KeyboardButton("/join"))
    bot.send_message(message.chat.id, 'Welcome!\nFind yourself an opponent!', reply_markup=markup)


@bot.message_handler(commands=['create'])
def handle_id_generator(message):
    print(str(message.chat.id) + ' ' + message.text)

    gameID = randrange(1000, 9999)
    while gameID in startedGamesID:
        gameID = randrange(1000, 9999)

    startedGamesID.add(str(gameID))

    updateUser(message.chat.id, status=Status.CREATE, game_id=gameID)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/cancel"))
    bot.send_message(message.chat.id, 'Your ID: {}, show it to your friend'.format(gameID), reply_markup=markup)


@bot.message_handler(commands=['join'])
def handle_join(message):
    print(str(message.chat.id) + ' ' + message.text)

    updateUser(message.chat.id, status=Status.JOIN)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("/cancel"))
    sent = bot.send_message(message.chat.id, 'Enter ID of friend: ', reply_markup=markup)
    bot.register_next_step_handler(sent, checkPin)


def checkPin(message):
    for i in startedGamesID:
        print(i)

    if message.text not in startedGamesID:
        bot.send_message(message.chat.id, 'This game is not found')
        handle_start(message)
    else:
        ###
        bot.send_message(message.chat.id, 'Game found!')
        bot.send_message(getOpponent(message.text, message.chat.id).chat_id, 'Game found!')
        updateUser(message.chat.id, Status.GAME, getUser(message.chat.id).game_id)
        updateUser(getOpponent(message.text, message.chat.id).chat_id, Status.GAME, getUser(message.chat.id).game_id)


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    try:
        getUser(message.chat.id)
    except Exception:
        updateUser(message.chat.id, status=Status.MAIN_MENU)
        handle_start(message)
        return
    if getUser(message.chat.id).status == Status.CREATE:
        startedGamesID.remove(getUser(message.chat.id).game_id)
        updateUser(message.chat.id, status=Status.MAIN_MENU)
        handle_start(message)
    elif getUser(message.chat.id).status == Status.JOIN:
        updateUser(message.chat.id, status=Status.MAIN_MENU)
        handle_start(message)


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
