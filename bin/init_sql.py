# -*- coding: utf-8 -*-
import os
import random
import urllib
import sqlite3
from resource.json_example import text1
from utils.models import RoomRecordBuilder
from utils.helper import get_date_period_id, get_now_period_id
from utils.constants import *
from settings import log, SQLITE_URL
# import time
# import simplejson as json


def test_select_sqlite():
    conn = sqlite3.connect(SQLITE_URL)
    c = conn.cursor()
    sql = """
    SELECT * FROM room
    """
    c.execute(sql)
    result = c.fetchall()
    c.close()
    conn.close()
    print(result, type(result))

def test_query_sqlite():
    conn = sqlite3.connect(SQLITE_URL)
    c = conn.cursor()
    try:
        # c.execute(sql_create_room)
        # c.execute(sql_create_roomsubtotal)
        # c.execute(sql_create_roomrecord)

        # c.execute(SQL_UPDATE_ROOMRECORD_BY_ID, (room_status['period_id'], current_time, status_record[0]))

        
        sql_str1 = """
        SELECT id, room_id, date_text, period_id, period_time, is_used, create_time, update_time FROM room_record where room_id = 1 and date_text = '2023-07-23' and period_id = 0;
        """

        sql_str2 = """
        SELECT id, room_id, date_text, period_id, period_time, is_used, create_time, update_time FROM room_record where room_id = %d and date_text = '%s' and period_id = %d;
        """ % (1, '2023-07-23', 0)

        # c.execute(SQL_FIND_ROOMRECORD_BY_PERIOD % (1, '2023-07-23', 0))
        print(sql_str2)
        c.execute(sql_str2)
        r = c.fetchone()
        print(type(r), r)
        print(r['id'], r['date_str'])
        conn.commit()
    except Exception as e:
        print(e)

    conn.commit()
    conn.close()



def test_create_table_sqlite():
    conn = sqlite3.connect(SQLITE_URL)
    c = conn.cursor()

    sql_create_room = """
    CREATE TABLE IF NOT EXISTS room ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        brand_id INTEGER, -- 小程序ID 初始化枚举值
        brand_name TEXT, -- 小程序品牌名 初始化枚举值
        store_id TEXT, -- 多店铺店铺ID 文本
        store_name TEXT, -- 多店铺店铺名称 文本
        room_ref_id TEXT, -- room_id 文本
        room_name TEXT, -- room_name 文本
        price_per_hour NUMERIC, -- price_per_hour 金额
        create_time DATETIME, -- create_time 时间
        update_time DATETIME -- update_time 时间
    );
    """

    sql_create_roomsubtotal = """
    CREATE TABLE IF NOT EXISTS room_subtotal ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        room_id INTEGER, -- 自记录的房间ID
        date_text TEXT, -- date_text 日期
        date_week NUMERIC, -- 星期
        price_per_hour NUMERIC, -- price_per_hour 金额
        used_hour NUMERIC, -- used_hour 数字
        amount NUMERIC, -- amount 金额
        create_time DATETIME, -- create_time 时间
        update_time DATETIME, -- update_time 时间
        CONSTRAINT unique_id_datetext UNIQUE (room_id, date_text)
    );
    """


    sql_create_roomrecord = """
    CREATE TABLE IF NOT EXISTS room_record ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- id 自增
        room_id INTEGER, -- 自记录的房间ID
        date_text TEXT, -- date_text 日期
        period_id INTEGER, -- 时段ID 0-47, 0 代表 00:00:00-00:30:00 依次类推 
        period_time TEXT, -- 时段,半小时记录 如 00:00-00:30
        is_used INTEGER, -- 是否预定 0 未预定， 1预定
        create_time DATETIME, -- create_time 时间
        update_time DATETIME, -- update_time 时间
        CONSTRAINT unique_id_datetext UNIQUE (room_id, date_text, period_id)
    );
    """

    sql_update_roomrecord = """
    INSERT INTO room_record (brand, room_name, room_id, date_text, price_per_hour, used_hour, amount, create_time, update_time) 
    VALUES
    ('{title}', '{author}', '{ad_url}', '{sd_url}', {down_status}, {created}, {updated});
    """



    # Create table
    try:
        # c.execute(sql_create_room)
        # c.execute(sql_create_roomsubtotal)
        # c.execute(sql_create_roomrecord)

        # c.execute(SQL_UPDATE_ROOMRECORD_BY_ID, (room_status['period_id'], current_time, status_record[0]))
        c.execute(SQL_FIND_ROOMRECORD_BY_PERIOD % (1, '2023-07-23', 0))
        r = c.fetchone()
        print(type(r), r)
        conn.commit()
    except Exception as e:
        print(e)


    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()





if __name__ == '__main__':
    
    test_select_sqlite()
    # test_create_table_sqlite()

    