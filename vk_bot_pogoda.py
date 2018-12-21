import vk_api
import requests
import bs4
from config import *
import random
import datetime
import time


def functional(user_id):
    vk_bot.method('messages.send', {'user_id': user_id,
                                    'message': 'Вот, что я умею:' + '\n' +
                                               '1) Установить город по умолчанию' + '\n' +
                                               '2) Отпраить погоду в определенном городе в определенный день.'
                                               'Для этого просто напиши "погода в" и название города.'
                                               'И еще одно правило! Я не понимаю беграмотных, поэтому пиши без ошибок!',
                                    'random_id': random.randint(0, 1000)})


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


def msg_weather(city, date):
    request = requests.get('https://sinoptik.com.ru/погода-' + city + '#' + date)
    b = bs4.BeautifulSoup(request.text, "html.parser")
    p3 = b.select('.temperature .p3')
    weather3 = p3[0].getText()
    p4 = b.select('.temperature .p4')
    weather4 = p4[0].getText()
    p5 = b.select('.temperature .p5')
    weather5 = p5[0].getText()
    p6 = b.select('.temperature .p6')
    weather6 = p6[0].getText()
    p7 = b.select('.temperature .p7')
    weather7 = p7[0].getText()
    p8 = b.select('.temperature .p8')
    weather8 = p8[0].getText()
    result = ('Утром: ' + weather3 + ' ' + weather4) + '\n'
    result += ('Днём: ' + weather5 + ' ' + weather6) + '\n'
    result += ('Вечером: ' + weather7 + ' ' + weather8) + '\n'
    temp = b.select('.rSide .description')
    weather = temp[0].getText()
    result += weather.strip()
    return result


vk_bot = vk_api.VkApi(token=TOKEN)

chosen_city = 0

day_name = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье']
today = datetime.datetime.now()
day = day_name[today.weekday()]
date = today.date()
p = 0

k = 0

while True:
    messages = vk_bot.method('messages.getConversations', {'filter': 'unread'})
    if messages['count'] >= 1:
        body = messages['items'][0]['last_message']['text']
        user_id = messages['items'][0]['last_message']['from_id']
        user_name = vk_bot.method('users.get', {'user_ids': user_id})
        if body.lower() == 'info':
            functional(user_id)

        # ----------------------------------Приветствие-----------------------------------------------------------------
        elif ('привет' in body.lower() or body.lower() == 'начать' or 'здравств' in body.lower()
              or body.lower() == 'кчау' or 'hello' in body.lower() or 'доров' in body.lower()
              or 'даров' in body.lower() or body.lower() == 'хай' or body.lower() == 'хэй' or body.lower() == 'йо'
              or body.lower() == 'йоу') and chosen_city == 0:
            write_msg(user_id, 'Привет, ' + (
                user_name[0]['first_name']) + '! Для того, чтобы ознакомиться с моим функционалом напиши info')
        # --------------------------------------------------------------------------------------------------------------

        # ---------------------------Определение города по умолчанию----------------------------------------------------
        elif body.lower() == 'установить город по умолчанию':
            chosen_city = 2
            write_msg(user_id, 'В каком городе ты живешь? Только давай без ошибок, а то ничего не получится!')
        elif chosen_city == 2:
            chosen_city = 0
            default_city = body = messages['items'][0]['last_message']['text']
            write_msg(user_id, 'Готово')
        # --------------------------------------------------------------------------------------------------------------

        # -------------------------Отправка сообщения для города по умолчанию-------------------------------------------
        elif day == 'Понедельник' and p == 0:
            p = 1
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Вторник' and p == 1:
            p = 2
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Среда' and p == 2:
            p = 3
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Четверг' and p == 3:
            p = 4
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Пятница' and p == 4:
            p = 5
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Суббота' and p == 5:
            p = 6
            write_msg(user_id, msg_weather(default_city, date))
        elif day == 'Воскресенье' and p == 6:
            p = 0
            write_msg(user_id, msg_weather(default_city, date))
        # --------------------------------------------------------------------------------------------------------------

        # -------------------Погода в определенном городе в определенный день-------------------------------------------
        elif 'погод' in body.lower():
            k = 1
            write_msg(user_id, 'Укажите город. Только давай без ошибок!!!')
        elif k == 1:
            k = 2
            city = messages['items'][0]['last_message']['text']
            write_msg(user_id, 'Если на сегодня, то так и напиши. Иначе введи дату в виде "гггг-мм-дд"')
        elif k == 2:
            k = 3
            date = messages['items'][0]['last_message']['text']
        elif k == 3:
            k = 0
            write_msg(user_id, msg_weather(city, date))
        # --------------------------------------------------------------------------------------------------------------
        elif chosen_city != 0:
            write_msg(user_id, 'Я тебя не понимаю. Напиши мне info, чтобы узнать, что я могу)')
