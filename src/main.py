import json

from flask import Flask, make_response, g
from apscheduler.schedulers.background import BackgroundScheduler
import to_json
import get_sheet_data
import psycopg2
import data_base
import requests
from my_functions import *

TOKEN = "5141013666:AAFDkri_oHLhSxP5fbu0qFEAgm_BDwZ2Hn4"
TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
MY_HEADER = {"Access-Control-Allow-Origin": "*"}
app = Flask(__name__)

dbase = None


@app.before_request
def before_request():
    """Получаем объект базы данных для дальнейшего использования"""
    global dbase
    db = get_db()
    dbase = data_base.DataBase(db)


def connect_db():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="vadim",
                                host="localhost",
                                database="test")
        return conn
    except Exception as e:
        print("Ошибка соединения с базой данных")
        exit()


def get_db():
    """Устанавливаем соединениее с БД через глобальную переменную g"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(exeption=None):
    """Закрываем соединениее с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/', methods=['GET'])
def home():
    """Функция-обработчик отвечающая за синхронизацию бд с google sheet и
    подгрузку данных в таблицу в виде json объекта"""
    table_data = get_sheet_data.get_sheet_data()
    dbase.sync_data(table_data)
    res_json = to_json.to_json_home(dbase)
    response = make_response((json.dumps(res_json),
                              200,
                              MY_HEADER))
    return response


@app.route('/chart', methods=['GET'])
def chart():
    """Функция-обработчик отвечающая за подгрузку данных в график в виде json объекта"""
    res_json = to_json.to_json_chart(dbase)
    response = make_response((json.dumps(res_json),
                              200,
                              MY_HEADER))
    return response


def background_sync():
    """Функция-обработчик отвечающая за автоматическую синхронизацию бд с google sheet"""
    with app.app_context():
        before_request()
        table_data = get_sheet_data.get_sheet_data()
        dbase.sync_data(table_data)
        close_db()
        print("synced")


def telegram_bot():
    """Функция-обработчик отвечающая за автоматическую проверку соблюдения «срока поставки» из таблицы.
        В случае, если срок прошел, скрипт отправляет уведомление в Telegram"""
    with app.app_context():
        before_request()
        res = dbase.get_out_of_date()
        message = prepare_message(res)
        my_dict = {"text": f"{message}", "chat_id": 427305163}
        requests.post(TELEGRAM_SEND_MESSAGE_URL, json=my_dict)
        close_db()
        print("sent")


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job1 = scheduler.add_job(background_sync, 'interval', minutes=10)
    job2 = scheduler.add_job(telegram_bot, 'interval', minutes=3600 * 12)
    scheduler.start()
    app.run(debug=True)
