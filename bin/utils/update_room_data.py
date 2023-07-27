# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from utils.helper import get_now_period_id
from utils.constants import *
import datetime
from settings import log, SQLITE_URL
import traceback


def udpate_db_roomrecord(room_arr, db=SQLITE_URL):
    # 写入日期与当前日期对比，影响房间记录时段的判断
    current_time = datetime.datetime.now()

    # 目标日期已过，不进行更新
    # if target_date < today:
    #     log.info('target date has passed, target_date: %s, today: %s' % (target_date, today))
    #     return
        
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:   
        for room_info in room_arr:

            date_str = room_info.date_text
            today = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            date_week = target_date.date().isoweekday()
            # 目标日期已过，不进行更新
            if target_date < today:
                log.info('target date has passed, target_date: %s, today: %s' % (target_date, today))
                continue 

            cur.execute(SQL_FIND_ROOM_ID % (room_info.store_id, room_info.room_ref_id))
            result = cur.fetchone()
            # print(result)
            # 查找是否存在房间信息，不存在就更新
            # print(vars(room_info), type(vars(room_info)))
            if result:
                room_info.room_id = result[0]
                # room_info.store_name = result[1]
            else:
                # room_info.store_name = 'New One ' + date_str
                # log.debug('room_info: %', vars(room_info))
                cur.execute(SQL_INSERT_ROOM, vars(room_info))
                conn.commit()
                cur.execute("SELECT last_insert_rowid()")
                new_insert_room = cur.fetchone()
                # print('new insert result -----------')
                # print(new_insert_room)
                room_info.room_id = new_insert_room[0]
            # print(room_info.room_id)
            # print(vars(room_info))
            # print('_____-----------------------')

            current_period = get_now_period_id()
            #开始更新房间记录表
            for room_status in room_info.status_list:
                cur.execute(SQL_FIND_ROOMRECORD_BY_PERIOD % (room_info.room_id, date_str, room_status['period_id']))
                status_record = cur.fetchone()
                if status_record:
                    # 更新状态数据
                    # 如果目标时间是当天且时间已过，不更新状态
                    if target_date == today and room_status['period_id'] <= current_period:
                        continue
                    # log.info('room record update, status_record: %s, room_status: %s' % (int(status_record[3]), room_status['period_id']))
                    # 如果使用状态不一致，则更新
                    if int(status_record[5]) != room_status['is_used']:
                        cur.execute(SQL_UPDATE_ROOMRECORD_BY_ID, (room_status['is_used'], current_time, status_record[0]))
                        conn.commit()
                        # log.info('room record update, room_record_id: %s, data: %s' % (status_record[0], room_status))
                else:
                    # 无历史更新数据则插入
                    room_status['room_id'] = room_info.room_id
                    room_status['date_text'] = date_str
                    room_status['create_time'] = current_time
                    room_status['update_time'] = current_time
                    # log.info('room record insert success, room_status: %s' % room_status)
                    cur.execute(SQL_INSERT_ROOMRECORD, room_status)
                    conn.commit()

            # 开始更新房间统计表
            # 封装 room_subtotal 字典
            room_subtotal = {'room_id': room_info.room_id,'store_id':room_info.store_id, 'date_text': date_str, 'date_week': date_week, 'price_per_hour': room_info.price_per_hour}
            # 获取当前房间状态统计值
            # cur.execute(SQL_FIND_ROOMRECORD_BY_DATETEXT % (room_info.room_id, date_str))
            # all_status = cur.fetchall()
            # used_half_hour = 0
            # for row in all_status:
            #     used_half_hour += row[3]
            cur.execute(SQL_SUM_ROOMRECORD_BY_DATETEXT % (room_info.room_id, date_str))
            used_half_hour = cur.fetchone()[0]
            room_subtotal['used_hour'] = used_half_hour / 2
            room_subtotal['amount'] = room_subtotal['used_hour'] * room_subtotal['price_per_hour']
            room_subtotal['create_time'] = current_time
            room_subtotal['update_time'] = current_time

            # log.info('test all subtotal count, room_subtotal: %s' % room_subtotal)

            # 如果有则更新记录，无则新增记录
            cur.execute(SQL_FIND_ROOMSUBTOTAL_BY_DATETEXT % (room_info.room_id, date_str))
            rst = cur.fetchone()
            if rst:
                # upddate
                cur.execute(SQL_UPDATE_ROOMSUBTOTAL_BY_ID, (room_subtotal['price_per_hour'], room_subtotal['used_hour'], room_subtotal['amount'], current_time, rst[0]))
                conn.commit()
            else:
                #insert
                cur.execute(SQL_INSERT_ROOMSUBTOTAL, room_subtotal)
                conn.commit()

            # log.info('test __dict__, room_subtotal: %s', room_subtotal)

        # log.info('duole room date update success')
        cur.close()
        conn.close()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())

if __name__ == '__main__':
    pass

