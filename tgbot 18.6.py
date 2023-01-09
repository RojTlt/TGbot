import telebot
from config import keys, TOKEN
from extensions import APIExeption, ValConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def startHelp(message: telebot.types.Message):
    text = 'Привет!' \
           '\nЯ бот-калькулятор для обмена валют.' \
           '\nПомогу тебе посчитать сколько ты сможешь выручить за продажу своих запасов крипты или фиата. Для этого просто введи' \
           ' два названия валют (продаваемую, покупаемую) и количество продаваемой в следующем формате:\nБиткоин Доллар 10' \
           '\n\nДля просмотра всех доступных валют введите команду /values' \
           '\n\nЕсли забудешь как мной пользоваться, просто введи команду /help'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def startHelp(message: telebot.types.Message):
    text = 'Чтобы узнать курс конвертации, введите две интересующих вас валюты - продаваемой и покупаемой, а также количество продаваемой.' \
           '\nНапример: Доллар Рубль 100' \
           '\n\nДля просмотра всех доступных валют введите команду /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def valuesList(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        mes = message.text.title().split(' ')
        if len(mes) != 3:
            raise APIExeption('Неверный формат сообщения.\n'\
                   'Пожалуйста, введите две валюты (продаваемая, покупаемая) и количество продаваемой, ориентируясь на следующий пример:\nДоллар Рубль 100')

        quote, base, amount = mes
        total_base = ValConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.send_message(message.chat.id, e)
    except Exception as e:
        bot.send_message(message.chat.id, e)
    else:
        sum = round(float(total_base) * float(amount), 3)
        text = f'При продаже {keys[quote]} в количестве {amount} единиц вы получите {sum} {keys[base]}.' \
               f'\nКурс обмена на данный момент: {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()