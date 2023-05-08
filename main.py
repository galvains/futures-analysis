import telebot
import pandas as pd

from time import time, sleep
from datetime import datetime
from binance.client import Client
from config import *


# Отправка уведомления боту
def send_pass(password: str) -> None:
    bot = telebot.TeleBot(BOT_TOKEN)
    bot.send_message(CHAT_ID, text=password)


# Проверка процента изменений цены
def get_info(current: float, middle: float) -> bool:
    return abs(middle - current) > middle / 100


def get_data(api_key: str, api_secret: str, symbol: str = 'ETHUSDT') -> None:

    while True:
        print(f"Start cycle ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})...")

        # получение времени прошлого часа в миллисекундах
        current_time_hour_ago = round(time() * 1000) - 3600000

        # создание клиента
        client = Client(api_key=api_key, api_secret=api_secret)

        # получение данных фьючерса
        coin = client.futures_historical_klines(
            symbol=symbol,
            interval='1m',
            start_str=current_time_hour_ago,
        )

        # создание датафрейма и запись в него колонки 'close' (цена закрытия фьючерса)
        df = pd.DataFrame()
        df['close'] = pd.DataFrame(coin).iloc[:, 4]
        middle_value = round(df['close'].astype(float).mean(), 2)
        current_value = float(df['close'].iloc[-2])

        print(df.tail(5))
        print(f'Middle: {middle_value}')

        # проверка на процентную разность (при выполнении - отправка уведомления)
        if get_info(current=current_value, middle=middle_value):
            send_pass(f'Attention! Quotes {symbol.upper()} changed by 1%')
            print('Attention! Quotes changed by 1%')

        sleep(60)


def main():
    symbol = input('Enter the futures to track (default: ETHUSDT)\n>>> ')

    if symbol:
        get_data(API_KEY, SECRET_KEY, symbol)
    else:
        get_data(API_KEY, SECRET_KEY)


if __name__ == '__main__':
    main()
