import requests
import json
from config import *

class APIExeption(Exception):
    pass

class ValConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIExeption(f'Конвертируемые валюты должны различаться. Нельзя перевести {keys[quote]} в {keys[quote]}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось найти запрашиваемую валюту - {quote}. Возможно Вы опечатались.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось найти запрашиваемую валюту - {base}. Возможно Вы опечатались.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество валюты - {amount}. ' \
                   f'\nДанный параметр необходимо вводить цифрами. Если Вы вводите дробное число,' \
                   f' то в качестве разделителя следует использовать "." точку.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base