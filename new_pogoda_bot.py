# import telebot
import requests
import datetime
from config import open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token="5829269251:AAHO3mDRG1cEzZCh-AYEmH5zyfJv8MW7pE8")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пиршлю сводку погоды!')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Cloyds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода!'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
              f'Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n'
              f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nВетер: {wind} м/с\n'
              f'Восход солнца: {sunrise_timestamp}\nЗакат солнца : {sunset_timestamp}\nПродолжительность дня : {length_of_the_day}\n'
              f'***ХОРОШЕГО ДНЯ!!!***'
              )

    except:
        await message.reply('\U00002620 Проверте название города \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)