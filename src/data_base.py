from my_functions import *
from cb_rf import get_price_in_rub


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_all(self):
        try:
            self.__cur.execute("SELECT * FROM test")
            res = self.__cur.fetchall()
            if res:
                return res

        except Exception as e:
            print(e)

    def get_one(self, row):
        try:
            self.__cur.execute(f"SELECT * FROM test WHERE '{row[1]}' = order_numb")
            res = self.__cur.fetchone()
            if res:
                return res

        except Exception as e:
            print(e)

    def insert_one(self, row):
        try:
            my_time = get_new_date(row[3])
            rub_cost = get_price_in_rub(row)
            self.__cur.execute(
                f"INSERT INTO test VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{rub_cost}', '{my_time}')")
            self.__db.commit()

        except Exception as e:
            print(e)

    def delete_one(self, row):
        try:
            self.__cur.execute(f"DELETE FROM test WHERE '{row[1]}' = order_numb")
            self.__db.commit()

        except Exception as e:
            print(e)

    def sync_data(self, table_data):
        list_of_values = table_data.get('values')[1:]
        all_db_data = self.get_all()
        if all_db_data == []:
            self.fill_db(list_of_values)
        else:
            self.update_db(list_of_values)
        self.delete_trash(all_db_data, list_of_values)

    def fill_db(self, list_of_values):
        for row in list_of_values:
            self.insert_one(row)

    def delete_trash(self, all_db_data, list_of_values):
        list_of_values = get_list_of_ord_numbs(list_of_values)
        for row in all_db_data:
            if not row[1] in list_of_values:
                self.delete_one(row)

    def update_db(self, list_of_values):
        for row_from_sheet in list_of_values:
            row_from_db = self.get_one(row_from_sheet)
            if row_from_db == None:
                self.insert_one(row_from_sheet)
            else:
                if not check_diff(row_from_sheet, row_from_db):
                    self.update_row(row_from_sheet)

    def update_row(self, row_from_sheet):
        try:
            self.__cur.execute(
                f"""UPDATE test 
                SET 
                numb = '{int(row_from_sheet[0])}',
                usd_cost = '{int(row_from_sheet[2])}',
                rub_cost = '{get_price_in_rub(row_from_sheet)}',
                delivery_time = '{row_from_sheet[3]}'
                WHERE order_numb = '{int(row_from_sheet[1])}'""")
            self.__db.commit()
        except Exception as e:
            print(e)
