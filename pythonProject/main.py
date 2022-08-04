import telebot

from config import *
from extentions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Добрый день,если хотите узнать курс валют, введите через пробел: ' \
           'количество, базовая валюта, валюта котировки'\
           'для просмотра доступных валют введите /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges:
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionException('Неверное число параметров')

        amount, quote, base = values

        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковую валюту')

        if quote not in exchanges or base not in exchanges:
            raise ConvertionException(f'Валюта вне доступного списка')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Неверный ввод количества')

        new_response_totals = Convertor.get_price(amount, quote, base)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {new_response_totals} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
