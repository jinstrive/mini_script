# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import random
import time
import requests
import sqlite3
import json
from utils.send_mail import warning_mail
from utils.constants import *
from utils.parse_data import parse_maheyou_status_data
from utils.update_room_data import udpate_db_roomrecord
from settings import log, SQLITE_URL, MAHEYOU_COOKIE, MAHEYOU_TIMESTAMP_PRIVATE
from utils.helper import get_json_from_resource_file
import traceback


def maheyou_request_data(store_id):

    # 定义URL变量
    URL = "https://api.5laoban.com/area/getplace"

    # 定义headers变量
    headers = {
        "Host": "api.5laoban.com",
        "referer": "https://servicewechat.com/wxfdb45a42427c3981/33/page-frame.html",
        "xweb_xhr": "1",
        "wxappid": "wxfdb45a42427c3981",
        "cookie": MAHEYOU_COOKIE,
        "version": "3.85.1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Language": "zh-CN,zh"
    }

    # 定义data变量
    data = {
        "timestamp_private": MAHEYOU_TIMESTAMP_PRIVATE,
        "wxapp": "1",
        "channel": "3",
        "store": store_id,
        "mid": "1572"
    }

    try:
        log.info('start to request maheyou data. store_id: %s' % store_id)
        response = requests.post(URL, headers=headers, data=data, verify=False)
        json_data = response.text
        # print(json_data)
        res = json.loads(json_data)
        if str(res['code']) == '100':
            return json_data
        else:
            log.warn('request duole failed. res: %s' % res)
            warning_mail('Request Maheyou Failed', res)
            return
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
    
    # print(type(response.text), response.text)

def maheyou_update_job(db=SQLITE_URL):

    # 获取所有麻合友的店铺进行更新
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT * FROM store WHERE brand_id = 2')
    # 先仅用杭州市店铺做测试
    # cur.execute("SELECT * from store where city = '杭州市'")

    maheyou_stores = cur.fetchall()
    

    for store in maheyou_stores:
        if not store:
            continue

        try:
            log.info('maheyou job: start to request and update room data. store: %s' % str(store))
            store_ref_id = store[3]
            if store_ref_id == '3864':
                # 如果是 测试店铺则跳过
                continue

            # 模拟测试数据
            # if store_ref_id != '3132':
            #     continue
            # json_data = json.dumps(get_json_from_resource_file('maheyou_room_status'))
            json_data = maheyou_request_data(store_ref_id)
            room_arr = parse_maheyou_status_data(json_data, store_ref_id, db)
            udpate_db_roomrecord(room_arr, db)
            log.info('maheyou job: update over, request and update room data. store_id: %s' % str(store))
            # Generate a random sleep duration between 2 and 5 seconds
            sleep_duration = random.uniform(1, 2)
            time.sleep(sleep_duration)
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            
    log.info('job-info: maheyou python done!')
    log.info('----------------------------------------------------')





if __name__ == '__main__':

    pass
