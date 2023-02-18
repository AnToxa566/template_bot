#main.py

import telebot
import io

from telebot import types

START = 'Start'

CREATE_TEMPLATE = 'Создать шаблон'
SET_CHANNEL = 'Установить канал'

SPOT = 'Спот'
FEAT = 'Фьючерсы'

HUOBI = 'Huobi'
BINANCE = 'Binance'

LIMIT = 'Limit'
MARKET = 'Market'

SHORT = 'Short'
LONG = 'Long'

WITH_SHITOC = '#crypto_signal_shitok'
WITHOUT_SHITOC = '#crypto_signal'

BACK = 'Назад'
EXIT = 'Выйти'

API_TOKEN = '5745924229:AAGgkSg5QUZstkQFJ7xkDCEOUwnBWJuzQ-0'
bot = telebot.TeleBot(API_TOKEN)

last_command = START

token = ''
exchange = ''
order_type =''
open_price = ''
average_price = ''

goalNum = 1
goals = []

link = ''
hashtag = ''

symbol_01 = ''
symbol_03 = ''
position_type = ''
stoploss = ''
buy_sell = ''
buy_sell_reverse = ''

def check_command(text, message):
    global last_command, exchange, order_type, hashtag, position_type, buy_sell, buy_sell_reverse, symbol_01, symbol_03
    
    if text == START:
        last_command = 'None'
        process_command(CREATE_TEMPLATE, SET_CHANNEL, from_message = message, send_message = 'Жду команду из меню команд 👇')
        
    elif text == CREATE_TEMPLATE:
        last_command = START
        process_command(SPOT, FEAT, from_message = message, send_message = 'Выберите тип торговли 👇')
        
    elif text == SET_CHANNEL:
        last_command = START
        set_channel(message)
    
    elif text == SPOT:
        last_command = CREATE_TEMPLATE
        process_command(BINANCE, HUOBI, from_message = message, send_message = 'Выберите биржу 👇', is_back = True)  
        
    elif text == FEAT:
        last_command = CREATE_TEMPLATE
        process_command(SHORT, LONG, from_message = message, send_message = 'Выберите позицию 👇', is_back = True)
        
    elif text == HUOBI or text == BINANCE:
        last_command = SPOT
        exchange = text
        
        if text == BINANCE:
            hashtag = WITHOUT_SHITOC
        else:
            hashtag = WITH_SHITOC
        
        process_command(LIMIT, MARKET, from_message = message, send_message = 'Выберите тип ордера 👇', is_back = True)
        
    elif text == LIMIT or text == MARKET:        
        order_type = text
        set_users_values(message)
        
    elif text == SHORT:
        last_command = FEAT
              
        symbol_01 = '🔻'
        symbol_03 = '🔽'
        position_type = 'SHORT'
        buy_sell = 'Продаем'
        buy_sell_reverse = 'Покупаем'
        
        set_users_values(message)
        
    elif text == LONG:
        last_command = FEAT
        
        symbol_01 = '🚀'
        symbol_03 = '🔼'
        position_type = 'LONG'
        buy_sell = 'Покупаем'
        buy_sell_reverse = 'Продаем'
        
        set_users_values(message)
        
    elif text == BACK:
        check_command(last_command, message)
        
    elif text == EXIT:
        check_command(START, message)


def set_channel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(EXIT)
    
    sent = bot.send_message(message.chat.id, """Для того, чтобы добавить возможность отправлять сообщения на канал, нужно выполнить следующие действия:
    
    1. Добавить на свой канал бота @myidbot с правами администратора. Он потребуется для получения id Вашего канала.
    2. Добавить текущего бота (@your_template_bot) в тот же канал, так же с правами администратора, чтобы у него была возможность отправлять сообщения на Ваш канал.
    3. Далее, на Вашем канале Вам следует вызвать команду /getgroupid. Вы получите сообщение с id Вашего канала. Скопируйте данный id и можете смело удалять сообщение.
    4. И, наконец, отправьте данный id прямо в этот чат""", reply_markup = markup)
    
    bot.register_next_step_handler(sent, set_channel_id)
    
    
def set_channel_id(message):
    if message.text != EXIT:
        user_id = str(message.from_user.id)
        
        with open("channel_id.txt", mode="r", encoding="utf-8") as file:
            file_data = file.read()
            file.seek(0, 0)
            lines = file.readlines()      
        
        if user_id in file_data:
            with open("channel_id.txt", mode="w", encoding="utf-8") as file:
                for line in lines:
                    if user_id not in line:
                        file.write(line)
                    else:
                        file.write(user_id + ' ' + message.text + '\n')
        else:
            with open("channel_id.txt", mode="a", encoding="utf-8") as file:
                file.write(user_id + ' ' + message.text + '\n')
        
        bot.send_message(message.chat.id, 'The channel has been added 🔥')
    
    check_command(START, message)
    

def set_users_values(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(EXIT)
    
    sent = bot.send_message(message.chat.id, 'Введите тикет токена', reply_markup = markup)
    bot.register_next_step_handler(sent, set_token)


def set_token(message):
    global token
     
    if message.text != EXIT:
        token = message.text
        sent = bot.send_message(message.chat.id, 'Введите цену открытия')
        bot.register_next_step_handler(sent, set_open_price)
    else:
        check_command(START, message)
    
def set_open_price(message):
    global open_price
    
    if message.text != EXIT:
        open_price = message.text
        sent = bot.send_message(message.chat.id, 'Введите цену усреднения')
        bot.register_next_step_handler(sent, set_average_price)
    else:
        check_command(START, message)
    
    
def set_average_price(message):
    global average_price, goals, goalNum
    
    if message.text != EXIT:
        average_price = message.text
        
        goals = []
        goalNum = 1
        
        sent = bot.send_message(message.chat.id, "Введите {}-ю цель".format(goalNum))
        bot.register_next_step_handler(sent, set_goal)
    else:
        check_command(START, message)
    
    
def set_goal(message):
    global goals, goalNum
    
    if message.text != EXIT:
        goals.append(message.text)
        goalNum = goalNum + 1
        
        if goalNum <= 5:
            sent = bot.send_message(message.chat.id, "Введите {}-ю цель".format(goalNum))
            bot.register_next_step_handler(sent, set_goal)
        elif last_command != FEAT:
            sent = bot.send_message(message.chat.id, 'Вставьте ссылку на Trading View')
            bot.register_next_step_handler(sent, set_link)
        else:
            sent = bot.send_message(message.chat.id, 'Введите стоплосс')
            bot.register_next_step_handler(sent, set_stoploss)
    else:
        check_command(START, message)


def set_stoploss(message):
    global stoploss
    
    if message.text != EXIT:
        stoploss = message.text
        sent = bot.send_message(message.chat.id, 'Вставьте ссылку на Trading View')
        bot.register_next_step_handler(sent, set_link)
    else:
        check_command(START, message)


def set_link(message):    
    global link
    
    if message.text != EXIT:
        link = message.text
        user_id = str(message.from_user.id)
        to_id = message.chat.id
        
        with open("channel_id.txt", mode="r", encoding="utf-8") as file:
            file_data = file.read()
            
            if user_id in file_data:
                file.seek(0, 0)
                lines = file.readlines()
                             
                for line in lines:
                    if user_id in line:
                        to_id = (line.split())[1]
                        break
        
        for i in 1, 2, 3:
            if last_command != FEAT: 
                spots = get_spots("spot_0{}.txt".format(i))
            else:
                spots = get_spots("feat_0{}.txt".format(i))
            
            bot.send_message(to_id, spots)
    
    bot.send_message(message.chat.id, 'Ready 🔥')
    check_command(START, message)


def process_command(*buttons, from_message, send_message, is_back = False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
    markup.add(*buttons)
    
    if is_back:
        markup.add(BACK)
        markup.add(EXIT)
    
    bot.send_message(from_message.chat.id, send_message, reply_markup = markup)


def get_spots(file_name):    
    file = io.open(file_name, mode="r", encoding="utf-8")
    filedata = file.read()
    file.close()
        
    return replace_filedata(filedata)


def replace_filedata(filedata):
    global token, exchange, order_type, open_price, average_price, goals, link, hashtag, symbol_01, symbol_03, position_type, buy_sell, buy_sell_reverse, stoploss
    
    filedata = filedata.replace('{token}', token)
    filedata = filedata.replace('{exchange}', exchange)
    filedata = filedata.replace('{order_type}', order_type)
    filedata = filedata.replace('{open_price}', open_price)
    filedata = filedata.replace('{average_price}', average_price)
    
    filedata = filedata.replace('{goal_01}', goals[0])
    filedata = filedata.replace('{goal_02}', goals[1])
    filedata = filedata.replace('{goal_03}', goals[2])
    filedata = filedata.replace('{goal_04}', goals[3])
    filedata = filedata.replace('{goal_05}', goals[4])
    
    filedata = filedata.replace('{link}', link)
    filedata = filedata.replace('{#}', hashtag)
    
    filedata = filedata.replace('{symbol_01}', symbol_01)
    filedata = filedata.replace('{symbol_03}', symbol_03)
    filedata = filedata.replace('{position_type}', position_type)
    filedata = filedata.replace('{buy_sell}', buy_sell)
    filedata = filedata.replace('{buy_sell_reverse}', buy_sell_reverse)
    filedata = filedata.replace('{stoploss}', stoploss)    
    
    return filedata


@bot.message_handler(commands = ['start'])
def start_message(message):
    check_command(START, message)


@bot.message_handler(content_types='text')
def message_reply(message):
    check_command(message.text, message)


bot.infinity_polling(timeout=10, long_polling_timeout = 5)