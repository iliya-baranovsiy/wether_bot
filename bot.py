import telebot
import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я бот для просмотра погоды, напиши город, в котором хочешь узнать погоду !)')


@bot.message_handler(content_types=['text'])
def wether_send(message):
    ans_message = None
    town = message.text
    querystring = {"q": town}

    headers = {
        "x-rapidapi-key": "1a48219c9cmsh25297f5786111c8p10e7cajsn645c6051af77",
        "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        res = response.json()
        loc = res['location']['name']
        temp = res['current']['temp_c'] + 5
        wind = int(res['current']['wind_kph'])
        hum = res['current']['humidity']
        cond = res['current']['cloud']
        if cond == 0:
            cond = 'Ясно'
        else:
            cond = 'Облачно'
        feels = res['current']['feelslike_c'] + 6
        ans = {
            'Город': loc,
            'Температура': temp,
            'Ветер': wind,
            'Влажность': hum,
            'Состояние': cond,
            'Ощущение': feels,
        }
        ans_message = f'Город:{ans['Город']}, {ans['Состояние']},Температура: {ans['Температура']}°C ,Ветер: {ans['Ветер']} км/ч, Влажность: {ans['Влажность']}, Ощущается как {ans['Ощущение']}°C'
    except:
        ans_message = 'Не нахожу такого города, возможно вы допустили ошибку при написании, попробуйте заново'

    bot.send_message(message.chat.id, ans_message)


bot.infinity_polling()
