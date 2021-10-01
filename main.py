import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Shahar nomini kiriting va sizga ob-havo ma'lumotini yuboraman! ")
    
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Botdan foydalanish uchun /start buyrug'ini kiriting!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Quyoshli \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'ir \U00002614",   
        "Drizzle": "Yomg'ir \U00002614",
        "Thunderstorm": "Bo'ron \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Derazaga qarang, men ob-havo qanday ekanligini tushunmayapman!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Bugungi sana: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Shahardagi ob -havo: {city}\nHarorat: {cur_weather}C° {wd}\n"
              f"Namlik: {humidity}%\nShamol: {wind} m/s\n"
              f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKunning uzunligi: {length_of_the_day}\n"
              )

    except:
        await message.reply("Afsuski bunday shahar topilmadi, shahar nomini tekshirib qaytadan yozing!")


if __name__ == '__main__':
    executor.start_polling(dp)