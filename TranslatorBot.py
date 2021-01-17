#Библиотеки
import telebot
import os
from google.cloud import translate_v2

#токен бота
bot = telebot.TeleBot('<bots Token>')

#шняга для работы переводчика
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'main folders path'


#глобальные переменные
glob_lang = 'en'
target = 'en'
langs = ['en', 'uk', 'ru']


#команда старт
@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Hi! I can translate your messages.\n' +  
        '3 target languages available\n(English, Ukrainian, Russian).' + 
        'Default target language is English\n'
        'To change language press /change.\n' +  
        'To get help press /help.'  
  )

#команда хелп
@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Message to developer', url = "https://t.me/sir_max778"  
  )  
    )  
    bot.send_message(  
        message.chat.id,  
        '1) This bot can translate your messages into 3 different languages.\n' +  
        '2) There are English, Ukrainian, Russian.\n' +  
        '3) This project is in beta.\n' + 
        '4) If you have any comments or suggestions, you can contact the developer using the link below.',  
        reply_markup=keyboard  
    )

#команда для смены языка
@bot.message_handler(commands=['change'])  
def exchange_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('English (En)', callback_data = 'get-en')  
    )  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('Ukrainian (Uk)', callback_data = 'get-uk'),  
        telebot.types.InlineKeyboardButton('Russian (Ru)', callback_data = 'get-ru')  
    )  
  
    bot.send_message(  
        message.chat.id,   
        'Click on the language of choice:',  
        reply_markup=keyboard  
    )


#тут идет какая-то крута хрень, ваще не шарю чо,
#но в общем что-то типа присвоения кнопкам языков нужных параметров
@bot.callback_query_handler(func=lambda call: True)  
def iq_callback(query):  
    data = query.data  
    if data.startswith('get-'):  
        get_ex_callback(query)

def get_ex_callback(query):  
    bot.answer_callback_query(query.id)  
    send_exchange_result(query.message, query.data[4:])

#вот именно тут идет присвоение
def send_exchange_result(message, ex_code):  
    bot.send_chat_action(message.chat.id, 'typing')  
    global target
    target = ex_code  
    bot.send_message(  
        message.chat.id, "Target language changed to " + ex_code.title() 
    )


#сам перевод сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):
    translate_client = translate_v2.Client()
    global target
    text = message.text
    output = translate_client.translate(
        text,
        target_language=target)
    print(output)
    bot.send_message(message.chat.id, output['translatedText'])


#обновление бота
bot.polling(none_stop=True)