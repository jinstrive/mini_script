# -*- coding: utf-8 -*-
import os
import sys
import random
import urllib
import time
import sqlite3
import json
from resource.json_example import text1
from utils.models import RoomRecordBuilder
from utils.helper import get_date_period_id, get_now_period_id, format_time
from utils.constants import *
import datetime
from settings import log, SQLITE_URL, SQLITE_TEST_URL
from utils.update_room_data import udpate_db_roomrecord
from jobs.maheyou_job import maheyou_update_job, maheyou_request_data

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
        """ % (
            1,
            "2023-07-23",
            0,
        )

        # c.execute(SQL_FIND_ROOMRECORD_BY_PERIOD % (1, '2023-07-23', 0))
        print(sql_str2)
        c.execute(sql_str2)
        r = c.fetchone()
        print(type(r), r)
        print(r["id"], r["date_str"])
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
        c.execute(SQL_FIND_ROOMRECORD_BY_PERIOD % (1, "2023-07-23", 0))
        r = c.fetchone()
        print(type(r), r)
        conn.commit()
    except Exception as e:
        print(e)

    # Insert a row of data
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # time_now = int(time.time())
    # sql_insert = sql_insert_exa.format(
    #     title='测试',
    #     author='爱德华',
    #     ad_url='ad_url',
    #     sd_url='sd_url',
    #     down_status=0,
    #     created=time_now,
    #     updated=time_now
    # )
    # print 'sql_insert == ', sql_insert
    # try:
    #     c.execute(sql_insert)
    # except Exception, e:

    #     print e

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def timetostr(dtime):
    # 导入datetime模块
    # import datetime
    # 获取当前时间的datetime对象
    # now = datetime.datetime.now()

    # 获取当前时间的时分秒
    hour = dtime.hour
    minute = dtime.minute
    second = dtime.second
    # 格式化成字符串，例如"14:03:38"
    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

    # 打印结果
    print(time_str)
    return time_str


def know_json():
    t_json = json.loads(text1)
    # print(t_json)
    for room in t_json["data"]:
        for key, value in room.items():
            print(key, value)

def get_time_range(n):
    start = datetime.datetime(2023, 2, 21, 0, 0, 0)
    end = start + datetime.timedelta(days=1)
    interval = (end - start) / 48
    
    start_dt = start + n * interval
    end_dt = start + (n+1) * interval
    
    start_time = start_dt.time().strftime("%H:%M:%S")
    end_time = end_dt.time().strftime("%H:%M:%S")
    
    return start_time, end_time

# def test_multargs(word, **kwargs):
def test_multargs(word, url='default'):
    print('==')
    print(word)
    print('-')
    print(url)

if __name__ == "__main__":
    # maheyou_request_data('2685')
    # maheyou_request_data('4400')
    # maheyou_update_job(SQLITE_TEST_URL)

    # test_multargs('Hey')
    # test_multargs('Hey, add kwargs', url={'a':1, 'b':2})
    # test_multargs({'a':1, 'b':2}, 'new url')

    # print(get_time_range(0))
    # print(get_time_range(15))
    # print(get_time_range(47))
    start = time.time ()
    args = sys.argv
    # print(args)
    # run_key = ""
    if len(args) > 2:
        run_key = args[1]
    # log.info("args type: %s, args: %s" % (type(args), args))
    log.info('path log success for mac and windows!')
    log.error('path log success for mac and windows!')
    end = time.time()
    log.info('count timeer: %s' % format_time(end-start))

    # execute the task based on the argument
    # match run_key:
    #     case "duole":
    #         print("duole")
    #     case "maheyou":
    #         print("maheyou")

    # timestamp = 1690213680
    # timestamp = 1690228080
    # timestamp = 1690214400
    # timestamp = 1690296000
    # timestamp = 1690296960315
    # 把时间戳转换为datetime对象
    # dt = datetime.datetime.fromtimestamp(timestamp)
    # 把datetime对象转换为指定格式的字符串
    # date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    # 打印或返回字符串
    # print(date_str)
