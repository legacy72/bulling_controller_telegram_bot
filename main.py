import logging

import telebot

from utils import get_info_about_bullying, get_arg
from settings import TELEGRAM_TOKEN

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
PERCENTAGE_BULLYING = 80
commands = {
    'help': 'Помощь по боту',
    'set_quality_percentage': 'Установить с какой вероятностью считать, что текст буллинговый (по умолчанию 80%)',
    'show_quality_percentage': 'Посмотреть при какой вероятности считать, что текст буллинговый',
}


@bot.message_handler(commands=['start', 'help'])
def start_and_help_handler(message):
    cid = message.chat.id
    help_text = 'Список команд: \n'
    for key in commands:
        help_text += f'/{key} : '
        help_text += f'{commands[key]}\n'
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['set_quality_percentage'])
def set_quality_percentage(message):
    try:
        percentage = get_arg(message.text)
        global PERCENTAGE_BULLYING
        PERCENTAGE_BULLYING = percentage
        bot.reply_to(
            message, f'Теперь сообщение будет считаться буллинговым при вероятности выше {PERCENTAGE_BULLYING}%'
        )
    except ValueError:
        bot.reply_to(message, 'Укажите через пробел число от 1 до 99')


@bot.message_handler(commands=['show_quality_percentage'])
def show_quality_percentage(message):
    bot.reply_to(
        message, f'Сообщения будут считаться буллинговым при вероятности выше {PERCENTAGE_BULLYING}%'
    )


@bot.message_handler(func=lambda message: True)
def check_bullers_handler(message):
    bulling_percentage, bad_words = get_info_about_bullying(message.text)
    if bulling_percentage > PERCENTAGE_BULLYING:
        bot.reply_to(
            message,
            f'Ты кибербуллер! Буллишь на {bulling_percentage}%. '
            f'В буллинговых текстах часто встречаются слова:\n{bad_words}'
        )


bot.polling()
