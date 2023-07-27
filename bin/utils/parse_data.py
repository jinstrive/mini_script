# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import datetime
from utils.models import RoomRecordBuilder
from utils.helper import get_date_period_id, get_timestr_from_period_id
from utils.constants import SQL_FIND_STORE_ID
from resource.json_example import text1
from settings import SQLITE_URL, log
import json
import sqlite3
import copy

def parse_duole_status_data(data, date_str, db=SQLITE_URL):
    # today = datetime.today()
    # today_date_str = today.strftime('%Y-%m-%d')
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    json_data = json.loads(data)
    room_arr = []
    # print(t_json)
    for origin_room in json_data['data']:
        room_info = RoomRecordBuilder('duole', origin_room['roomId'], date_str)

        # 从数据库中找store_id   
        cur.execute(SQL_FIND_STORE_ID % (room_info.brand_id, origin_room['storeId']))
        res = cur.fetchone()
        if res:
            room_info.store_id = res[0]
        else:
            # 先保障跑下去，再进行修复
            log.error('Store not find, use the refer store_id, room_info: %s, data_room: %s' % (room_info, origin_room))
            room_info.store_id = origin_room['storeId']

        # room_info.store_name = origin_room['storeName']
        room_info.room_name = origin_room['roomName']
        room_info.price_per_hour = float(origin_room['roomPrice'])
        # "createTime": "2023-04-09 13:50:43",
        room_info.create_time = datetime.datetime.strptime(origin_room['createTime'], "%Y-%m-%d %H:%M:%S")
        room_info.update_time = datetime.datetime.strptime(origin_room['updateTime'], "%Y-%m-%d %H:%M:%S")
        room_info.status_list = []
        for origin_room_status in origin_room['roomStatusList']:
            room_status = {}
            room_status['period_id'] = get_date_period_id(origin_room_status['startTime'])
            room_status['period_time'] = origin_room_status['startTime']
            room_status['start_time'] = origin_room_status['startTime']
            room_status['end_time'] = origin_room_status['endTime']
            room_status['is_used'] = 0 if origin_room_status['available'] else 1 
            room_info.status_list.append(room_status)
        room_arr.append(room_info)


    cur.close()
    conn.close()
    
    return room_arr


def parse_maheyou_status_data(data, store_ref_id, db=SQLITE_URL):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    json_data = json.loads(data)

    timestamp = json_data['result']['start']
    query_time = datetime.datetime.fromtimestamp(timestamp)
    date_str = query_time.strftime("%Y-%m-%d")

    room_arr = []
    places = json_data['result']['area'][0]['place']
    # print(t_json)
    for origin_room in places:

        if origin_room['fname'] == '停业':
            log.info('Room Stop, not record, data_room: %s' % (origin_room))
            continue

        room_info = RoomRecordBuilder('maheyou', origin_room['pid'], date_str)
        # 从数据库中找store_id   
        cur.execute(SQL_FIND_STORE_ID % (room_info.brand_id, store_ref_id))
        res = cur.fetchone()
        if res:
            room_info.store_id = res[0]
        else:
            # 先保障跑下去，再进行修复
            log.error('Store not find, use the refer store_id, room_info: %s, data_room: %s' % (room_info, origin_room))
            room_info.store_id = origin_room['pid']

        # room_info.store_name = origin_room['storeName']
        room_info.room_name = origin_room['title']
        room_info.price_per_hour = float(origin_room['price']) / 100
        # "createTime": "2023-04-09 13:50:43",
        room_info.create_time = query_time
        room_info.update_time = query_time
        room_info.status_list = []

        next_room_info = copy.deepcopy(room_info)
        next_day = query_time + datetime.timedelta(days=1)
        next_room_info.date_text = next_day.strftime('%Y-%m-%d')

        is_next_room = False

        for tl in origin_room['timeline']:
            timeline_key = tl['key']
            period = 0
            if timeline_key == '次':
                is_next_room = True
            else:
                period = timeline_key

            period_id_1 = period * 2
            period_id_2 =  period_id_1 + 1

            is_used = 1 if tl['val'] else 0

            # 开始组装占用时段

            room_status1 = {}
            room_status1['period_id'] = period_id_1
            room_status1['start_time'], room_status1['end_time'] = get_timestr_from_period_id(period_id_1)
            room_status1['period_time'] = room_status1['start_time']
            room_status1['is_used'] = is_used


            room_status2 = {}
            room_status2['period_id'] = period_id_2
            room_status2['start_time'], room_status2['end_time'] = get_timestr_from_period_id(period_id_2)
            room_status2['period_time'] = room_status2['start_time']
            room_status2['is_used'] = is_used

            if not is_next_room:
                room_info.status_list.append(room_status1)
                room_info.status_list.append(room_status2)
            else:
                next_room_info.status_list.append(room_status1)
                next_room_info.status_list.append(room_status2)

        room_arr.append(room_info)

        if is_next_room:
            room_arr.append(next_room_info)

    cur.close()
    conn.close()

    return room_arr
    




if __name__ == '__main__':
    

    objs = parse_duole_status_data(text1, '2023-07-22')