import datetime


def check_diff(row_from_sheet, row_from_db):
    bool = int(row_from_sheet[0]) == row_from_db[0] and \
           int(row_from_sheet[2]) == row_from_db[2] and \
           get_new_date(row_from_sheet[3]) == str(row_from_db[4])
    return bool


def get_new_date(str_date):
    return "-".join(str_date.split(".")[::-1])


def get_date_for_comp(str_date):
    return "-".join(str_date.split("/")[::-1])


def get_now_date():
    now_data = str(datetime.datetime.now()).split()[0]
    return "/".join(now_data.split("-")[::-1])


def get_date_for_req(str_date):
    return str_date.replace(".", "/")


def get_str_date(all_date):
    for x in all_date:
        x[4] = str(x[4])
    return all_date


def get_list_of_ord_numbs(list_of_values):
    return list(map(lambda x: int(x[1]), list_of_values))
