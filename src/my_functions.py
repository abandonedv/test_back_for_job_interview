import time

from cb_rf import *
import datetime


def check_del_date(new_time, old_time):
    return new_time == old_time


def get_new_date(row):
    return "-".join(row[3].split(".")[::-1])


def get_date_for_req(row):
    return row[3].replace(".", "/")


def get_str_date(all_date):
    for x in all_date:
        x[4] = str(x[4])
    return all_date


def get_rate_float(date):
    str_rate = get_rate(date)
    float_rate = float(str_rate.replace(",", "."))
    return float_rate


def get_price_in_rub(row):
    date = get_date_for_req(row)
    rate = get_rate_float(date)
    price = float(row[2])
    return price * rate


def get_list_of_ord_numbs(list_of_values):
    return list(map(lambda x: int(x[1]), list_of_values))

# def get_seconds(date):
#     date_list = list(map(int, date.split("-")))
#     res_date = datetime.datetime(*date_list)
#     sec = res_date.timestamp()
#     return sec * 1000
