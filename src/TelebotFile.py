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
    GAME = 3


class User:
    def __init__(self, chat_id, status=Status.MAIN_MENU, game_id=0, message=None, points=0):
        self.chat_id = chat_id
        self.status = status
        self.game_id = game_id
        self.message = message
        self.points = points


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


def updateUser(chat_id, status=Status.MAIN_MENU, game_id=0, message=None, points=0):
    if message is None and userSet.get(chat_id) is not None:
        userSet.update({chat_id: User(chat_id, status, str(game_id), userSet[chat_id].message, points)})
    else:
        userSet.update({chat_id: User(chat_id, status, str(game_id), message, points)})


@bot.message_handler(commands=['start'])
def handle_start(message):
    print(str(message.chat.id) + ' ' + message.text)

    updateUser(message.chat.id, status=Status.MAIN_MENU, message=message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("/create"))
    markup.row(types.KeyboardButton("/join"))
    bot.send_message(message.chat.id, 'Welcome!\nFind yourself an opponent!', reply_markup=markup)


@bot.message_handler(commands=['create'])
def handle_id_generator(message):
    print(str(message.chat.id) + ' ' + message.text)

    gameID = randrange(1000, 10000)
    while gameID in startedGamesID:
        gameID = randrange(1000, 10000)

    startedGamesID.add(str(gameID))

    updateUser(message.chat.id, status=Status.CREATE, game_id=gameID, message=message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/cancel"))
    bot.send_message(message.chat.id, 'Your ID: {}, show it to your friend'.format(gameID), reply_markup=markup)


@bot.message_handler(commands=['join'])
def handle_join(message):
    print(str(message.chat.id) + ' ' + message.text)

    updateUser(message.chat.id, status=Status.JOIN, message=message)

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
        preGame(getUser(message.chat.id), getOpponent(getUser(message.chat.id).game_id, message.chat.id))


def preGame(player1, player2):
    # if player1.points >= 5 or player2.points >= 2:
    #     raise Exception('coming soon')
    a1 = [randrange(10, 100) for i in range(20)]
    b1 = [randrange(10, 100) for i in range(20)]
    c1 = [randrange(0, 3) for i in range(20)]
    a2 = a1.copy()
    b2 = b1.copy()
    c2 = c1.copy()
    game(player1, player2, a1, b1, c1)
    game(player2, player1, a2, b2, c2)


def game(player, opponent, a, b, c):
    if getUser(player.chat_id).points >= 5 and getOpponent(opponent.game_id, player.chat_id).points >= 5:
        bot.send_message(player.chat_id, 'Draw!')

        bot.clear_step_handler(player.message)
        bot.clear_step_handler(opponent.message)

        handle_start(player.message)

        if player.game_id in startedGamesID:
            startedGamesID.remove(player.game_id)

        updateUser(player.chat_id, Status.MAIN_MENU, 0, None, 0)
        updateUser(opponent.chat_id, Status.MAIN_MENU, 0, None, 0)

        return

    elif getUser(player.chat_id).points >= 5 >= 5:
        bot.send_message(opponent.chat_id, 'You Lose!')
        bot.send_message(player.chat_id, 'You Win!')

        bot.clear_step_handler(player.message)
        bot.clear_step_handler(opponent.message)

        handle_start(player.message)
        handle_start(opponent.message)

        if player.game_id in startedGamesID:
            startedGamesID.remove(player.game_id)

        updateUser(player.chat_id, Status.MAIN_MENU, 0, None, 0)
        updateUser(opponent.chat_id, Status.MAIN_MENU, 0, None, 0)

        return

    # markup = types.InlineKeyboardMarkup()
    # item1 = types.InlineKeyboardButton("1", callback_data="1")
    # item2 = types.InlineKeyboardButton("2", callback_data="2")
    # item3 = types.InlineKeyboardButton("3", callback_data="3")
    # item4 = types.InlineKeyboardButton("4", callback_data="4")
    # item5 = types.InlineKeyboardButton("5", callback_data="5")
    # item6 = types.InlineKeyboardButton("6", callback_data="6")
    # item7 = types.InlineKeyboardButton("7", callback_data="7")
    # item8 = types.InlineKeyboardButton("8", callback_data="8")
    # item9 = types.InlineKeyboardButton("9", callback_data="9")
    # #itemX = types.InlineKeyboardButton("/cancel")
    # item0 = types.InlineKeyboardButton("0", callback_data="0")
    # #itemOK = types.InlineKeyboardButton("OK")
    # markup.row(item1, item2, item3)
    # markup.row(item4, item5, item6)
    # markup.row(item7, item8, item9)
    # markup.row(item0)

    if c[0] == 0:
        sent = bot.send_message(player.chat_id, "{} + {} = ?".format(a[0], b[0]), reply_markup=None)
        bot.register_next_step_handler(sent, answerFun, a[0] + b[0], opponent, a, b, c)
    elif c[0] == 1:
        sent = bot.send_message(player.chat_id, "{} - {} = ?".format(max(a[0], b[0]), min(a[0], b[0])), reply_markup=None)
        bot.register_next_step_handler(sent, answerFun, max(a[0], b[0]) - min(a[0], b[0]), opponent, a, b, c)
    elif c[0] == 2:
        sent = bot.send_message(player.chat_id, "{} * {} = ?".format(a[0], b[0] % 10 + 1), reply_markup=None)
        bot.register_next_step_handler(sent, answerFun, a[0] * (b[0] % 10 + 1), opponent, a, b, c)


def answerFun(message, answer, opponent, a, b, c):
    if message.text == str(answer):
        updateUser(message.chat.id, status=Status.GAME, game_id=opponent.game_id, message=message,
                   points=getUser(message.chat.id).points + 1)

        bot.send_message(opponent.chat_id, 'Opponent decided right ({}/5)'.format(getUser(message.chat.id).points))
        bot.send_message(message.chat.id, 'Right! You have ({}/5) points!'.format(getUser(message.chat.id).points))
    else:
        bot.send_message(opponent.chat_id, 'Opponent decided wrong ({}/5)'.format(getUser(message.chat.id).points))
        bot.send_message(message.chat.id, 'Wrong! You have ({}/5) points!'
                                          ' Answer: {}'.format(getUser(message.chat.id).points, answer))
    a.pop(0)
    b.pop(0)
    c.pop(0)
    game(getUser(message.chat.id), opponent, a, b, c)


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
    elif getUser(message.chat.id).status == Status.GAME:

        opponent = getOpponent(getUser(message.chat.id).game_id, message.chat.id)

        bot.send_message(message.chat.id, 'Game stopped!')
        bot.send_message(opponent.chat_id, 'Game stopped!')

        updateUser(opponent.chat_id,
                   Status.MAIN_MENU)
        updateUser(message.chat.id, Status.MAIN_MENU)

        handle_start(opponent.message)
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
