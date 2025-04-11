import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from core import bot

bot = telebot.TeleBot("6776934179:AAFAbjN0zWfdOLFgHRh9uTQHcKBPkHXWujY")


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    username = message.from_user.username
    bot.send_message(chat_id=message.chat.id,
                     text=f"Привет, {username}, это бот для бесплатного просмотра фильмов, введи название любого фильма)")


@bot.message_handler(content_types=["text"])
def find_film(message: telebot.types.Message):
    text = message.text
    text = text.replace(' ', '+')
    url = f" https://www.kinopoisk.ru/index.php?kp_query={text}"
    response = requests.get(url)
    try:
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            most_wanted = soup.find_all('div', class_='element most_wanted')[0]
            block_with_url = str(most_wanted.find_all('p')[0])
            start_index = block_with_url.find('href')
            end_index = block_with_url.find('sr/1/')
            film_code = block_with_url[start_index + 7:end_index]
            url_to_watch = f"www.kinopoisk.gg/{film_code}"
            print(message.from_user.username)
            print(text)

            data = most_wanted.find_all('a')
            for i in data:
                if 'постеры' in i:
                    poster_url = f" https://www.kinopoisk.ru{i['data-url']}"

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('ссылка', url=url_to_watch))
        bot.send_message(chat_id=message.chat.id, text=f"Вот ссылка", reply_markup=keyboard)
    except:
        bot.send_message(chat_id=message.chat.id, text=f"Фильм не найден")
        print(message.from_user.username)
        print(text)


bot.infinity_polling()
