from config import TOKEN_TELEGRAM, TOKEN_API_WEATHER
import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN_TELEGRAM)
deaspetcher = Dispatcher(bot)

@deaspetcher.message_handler(commands=["start"])
async def smart_comand(message:types.Message):
    await message.reply("Привет, напиши мне название города и я пришлю сводку по погоде")


@deaspetcher.message_handler()
async def get_weather(message:types.Message):
    code_to_smile = {
        "Clear": "Ясно ",
        "Clouds": "Облачно",
        "Snow": "Снег",
        "Rain": "Дождь",
        "Thunderstorm": "Гроза",
        "Orizzle": "Дождь",
        "Mist": "Туман"
    }
    try:
        responce = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={TOKEN_API_WEATHER}&units=metric")
        data = responce.json()
        city = data["name"]
        weather = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        format = "%Y-%m-%d %H:%M"
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            weather_description = code_to_smile[weather_description]
        else:
            weather_description = weather_description
        await message.reply(f"********* {datetime.datetime.now().strftime(format)} ***********\n"
                            f"В городе:{city}\n Погода:{weather_description}\n "
              f"Температура:{weather}°C\n Скорость ветра:{wind_speed} м/c\n Рассвет:{sunrise}\n Закат:{sunset}")
    except Exception as exc:
        print(exc)
        await message.reply("Вы ввели неправельно город")

if __name__ == "__main__":
    executor.start_polling(deaspetcher)