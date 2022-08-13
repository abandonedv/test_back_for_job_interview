import requests
from xml.etree import ElementTree
from my_functions import *


def get_rate(row_time):
    """Функция совершающая get-запрос к ЦБ РФ API для получения курса доллара к рублю"""
    if get_date_for_comp(row_time) > get_date_for_comp(get_now_date()):
        row_time = get_now_slash_date()
    response = requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={row_time}", stream=True)

    response.raw.decode_content = True

    root = ElementTree.parse(response.raw)

    usd = root.find("./Valute[@ID='R01235']")
    usd_value = usd.find("Value")
    return usd_value.text


def get_rate_float(date):
    """Функция позволяющая перевести курса доллара к рублю в float"""
    str_rate = get_rate(date)
    float_rate = float(str_rate.replace(",", "."))
    return float_rate


def get_price_in_rub(row):
    """Функция позволяющая узнать цену заказа в рублях на основе строки заказа"""
    date = get_date_for_req(row[3])
    rate = get_rate_float(date)
    price = float(row[2])
    return price * rate
