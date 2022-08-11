from my_functions import *


def to_json_home(dbase):
    all_data_from_db = dbase.get_all()
    all_data = get_str_date(list(map(list, all_data_from_db)))
    my_json = {"values": all_data}
    return my_json


def to_json_chart(dbase):
    all_data_from_db = dbase.get_all()
    all_data = get_str_date(list(map(list, all_data_from_db)))
    chart_list = [[row[0], row[4], row[2]] for row in all_data]
    my_json = {"values": chart_list}
    return my_json

