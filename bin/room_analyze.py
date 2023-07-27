# -*- coding: utf-8 -*-
import os
import sys
import csv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
import sqlite3
from utils.constants import *
import datetime
from settings import log, SQLITE_URL


def get_all_room_subtotal_steps():
    conn = sqlite3.connect(SQLITE_URL)
    cur = conn.cursor()

    try:
        # Define the path and filename for the CSV file
        f_name = "allrooms_%s.csv" % datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        csv_file = Path(__file__).parent.parent / "outputs" / f_name
        data_dict = {
            'date_text': '',
            'date_week': '',
            'room_id': '',
            # 'room_name': '',
            'store_id': '',
            'store_name': '',
            'brand_name': '',
            'price_per_hour': '',
            'used_hour': '',
            'amount': '',
            'province': '',
            'city': '',
        }
        # Write the all_roomtotal_datas dictionary into the CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=data_dict.keys())
            writer.writeheader()

            # 以店铺维度进行循环获取数据，并写入文件中
            cur.execute('select * from store')
            stores = cur.fetchall()

            for store in stores:

                store_id = store[0]
                data_dict['store_id'] = store_id
                data_dict['store_name'] = store[4]
                data_dict['brand_name'] = store[2]
                data_dict['province'] = store[5]
                data_dict['city'] = store[6]

                # 通过店铺获取到所有的房间记录
                cur.execute("select * from room_subtotal where store_id = '%s'" % store_id)
                room_subtotals = cur.fetchall()

                for room_subtotal in room_subtotals:
                    data_dict['room_id'] = room_subtotal[1]
                    data_dict['date_text'] = room_subtotal[2]
                    data_dict['date_week'] = room_subtotal[3]
                    data_dict['price_per_hour'] = room_subtotal[4]
                    data_dict['used_hour'] = room_subtotal[5]
                    data_dict['amount'] = room_subtotal[6]

                    writer.writerow(data_dict)

            # writer.writerows(all_roomtotal_datas)

        
        # print(all_roomtotal_datas[0])
        # print(all_roomtaotal_datas)
        # pairs = zip(col_names, all_subtotal)
        # for room_subtotal in all_subtotal:
            # print(room_subtotal)
    except Exception as e:
        log.error(e)

    cur.close()
    conn.close()

def get_all_room_subtotal():
    conn = sqlite3.connect(SQLITE_URL)
    cur = conn.cursor()

    try:
        # 获取所有房间信息
        cur.execute(SQL_FIND_ALL_ROOM)
        room_col_names = [description[0] for description in cur.description]
        room_arr = cur.fetchall()
        # all_room_datas = list(map(lambda row: dict(zip(room_col_names, row)), room_arr))
        all_room_datas = list(map(lambda row: dict(zip(room_col_names, row)), room_arr))
        all_room_datas_dict = dict(map(lambda d: (str(d["id"]), d), all_room_datas))
        # print(all_room_datas_dict)
        # print(all_room_datas_dict.get('1'))
        # 获取所有房间小计数据
        cur.execute(SQL_FIND_ALL_ROOMSUBTOTAL)

        col_names = [description[0] for description in cur.description]
        roomtotal_arr = cur.fetchall()
        all_roomtotal_datas = list(map(lambda row: dict(zip(col_names, row)), roomtotal_arr))
        for rtotal in all_roomtotal_datas:
            rtotal['brand_name'] = all_room_datas_dict.get(str(rtotal['room_id'])).get('brand_name') 
            rtotal['room_name'] = all_room_datas_dict.get(str(rtotal['room_id'])).get('room_name') 

        # Define the path and filename for the CSV file
        csv_file = "test_%s.csv" % datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        # Write the all_roomtotal_datas dictionary into the CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=all_roomtotal_datas[0].keys())
            writer.writeheader()
            writer.writerows(all_roomtotal_datas)
        
        # print(all_roomtotal_datas[0])
        # print(all_roomtaotal_datas)
        # pairs = zip(col_names, all_subtotal)
        # for room_subtotal in all_subtotal:
            # print(room_subtotal)
    except Exception as e:
        log.error(e)

    cur.close()
    conn.close()

if __name__ == '__main__':
    # get_all_room_subtotal()

    # f_name = "allrooms_%s.csv" % datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    # csv_file = Path(__file__).parent.parent / "outputs" / f_name
    # print(csv_file)
    get_all_room_subtotal_steps()

