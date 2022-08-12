import json

from flask import Flask, make_response, g
from apscheduler.schedulers.background import BackgroundScheduler
import to_json
import get_sheet_data
import psycopg2
import data_base

MY_HEADER = {"Access-Control-Allow-Origin": "*"}
app = Flask(__name__)

dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = data_base.DataBase(db)


def connect_db():
    conn = psycopg2.connect(user="postgres",
                            password="vadim",
                            host="localhost",
                            database="test")
    return conn


def get_db():
    """Устанавливаем соединениее с БД через глобальную переменную g"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(exception=None):
    """Закрываем соединениее с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/', methods=['GET'])
def home():
    table_data = get_sheet_data.get_sheet_data()
    dbase.sync_data(table_data)
    res_json = to_json.to_json_home(dbase)
    response = make_response((json.dumps(res_json),
                              200,
                              MY_HEADER))
    return response


@app.route('/chart', methods=['GET'])
def chart():
    res_json = to_json.to_json_chart(dbase)
    response = make_response((json.dumps(res_json),
                              200,
                              MY_HEADER))
    return response


def background_sync():
    with app.app_context():
        before_request()
        table_data = get_sheet_data.get_sheet_data()
        dbase.sync_data(table_data)
        close_db()
        print("synced")


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(background_sync, 'interval', minutes=10)
    scheduler.start()
    app.run(debug=True)
