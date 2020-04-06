import telebot
from config import token
from parser import get_data

bot = telebot.TeleBot(token)
countries = ('Russia', 'Italy', 'USA')


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(*countries)
    bot.send_message(message.chat.id, "Выбери срану из списка:", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def command_country(message):
    if message.text in countries:
        data = get_data(message.text)
        msg = f"Всего случаев: {data['total_cases']}\n" \
              f"Новых случаев: {data['new_cases']}\n" \
              f"Всего смертей: {data['total_deaths']}\n" \
              f"Динамика смертей: {data['new_deaths']}\n" \
              f"Всего вылечившихся: {data['total_recovered']}\n"
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, 'Выберите странну из списка:')


if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=0)
