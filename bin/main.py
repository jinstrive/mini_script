# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import random
import time
import requests
import json
from utils.helper import get_current_date, format_time
from utils.send_mail import warning_mail
from utils.constants import *
from utils.parse_data import parse_duole_status_data
from jobs.maheyou_job import maheyou_update_job
from utils.update_room_data import udpate_db_roomrecord
import datetime
from settings import log, SQLITE_URL, SQLITE_TEST_URL
import traceback


DUOLE_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3eG1lbWJlci0xNzk1NTUiLCJpYXQiOjE2OTAxNjg4NDYsImV4cCI6MTY5MDc3MzY0Nn0.iOd1FFosbI7rMZkDVqkjXsWByX7ZrmaXCZ8Dxo9J06FllW3hHPvPZB8n4gkNAA4kiowbCk_kBOMnF_5kitKwKA"

def duole_request_data(store_id, date_str):
    headers = {
    "Host": "prod.iyuecha.net",
    "referer": "https://servicewechat.com/wx3b8820e460c0127c/6/page-frame.html",
    "xweb_xhr": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
    "token": DUOLE_TOKEN,
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Language": "zh-CN,zh"
    }
    duole_req_dict = {
        'store_id': store_id,
        'date_str' : date_str
    }
    url = "https://prod.iyuecha.net/thapi/app/room/get-room-list/v1?storeId={store_id}&orderDate={date_str}".format(**duole_req_dict)
    try:
        log.info('start to request duole data. date_str: %s, store_id: %s' % (date_str, store_id))
        response = requests.get(url, headers)
        json_data = response.text
        # print(json_data)
        res = json.loads(json_data)
        if res['msg'] == 'success':
            log.info('request duole successful. msg: %s' % res['msg'])
            return json_data
        else:
            log.warn('request duole failed. msg: %s' % res['msg'])
            warning_mail('Request Duole Failed', res)
            return
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
    
    # print(type(response.text), response.text)

def duole_update_job():
    date_str_arr = []
    date_str_arr.append(get_current_date())
    # 晚上9点后，开始获取第二天的数据

    current_time = datetime.datetime.now()
    if current_time.hour >= 21:
        # 获取明天的日期
        tomorrow = current_time + datetime.timedelta(days=1)
        # 格式化为字符串，你可以根据需要修改格式
        tom_str = tomorrow.strftime("%Y-%m-%d")
        date_str_arr.append(tom_str)


    # 执行curl，获取json数据
    for date_str in date_str_arr:
        if not date_str:
            continue

        # for store_id in (177, ):
        for store_id in (177, 178):
            try:
                log.info('duole job: start to request and update duole room data. store_id: %s, date_str: %s' % (store_id, date_str))

                json_data = duole_request_data(store_id, date_str)
                # json_data = text_20230724
                data = parse_duole_status_data(json_data, date_str)
                udpate_db_roomrecord(data)
                log.info('duole job: update over, request and update duole room data. store_id: %s, date_str: %s' % (store_id, date_str))

                # Generate a random sleep duration between 2 and 5 seconds
                sleep_duration = random.uniform(2, 5)
                time.sleep(sleep_duration)
            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
        
    log.info('job-info: duole python done! date_str: %s' % date_str_arr)
    log.info('----------------------------------------------------')


def start_update_room_job(job_name):
    current_time = datetime.datetime.now()
    # 记录程序开始的时间
    start = time.time ()
    # 模拟访问时间，2点到9点之间不发请求
    if 2 <= current_time.hour < 9:
        log.info('###### job stop. Simulate normal user access time. Now:%s, Hour:%s' % (current_time, current_time.hour))
        return

    match job_name:
        case "duole":
            log.info('###### job start --- duole ---. ')
            duole_update_job()
        case "maheyou":
            log.info('###### job start --- maheyou ---. ')
            maheyou_update_job()
    
    # 记录程序结束的时间
    end = time.time ()
    log.info('###### job over. --- the job taken times: %s' % format_time(end - start))
    
    # duole_update_job()




if __name__ == '__main__':

    args = sys.argv
    # job_name = 'maheyou'
    job_name = 'duole'
    if len(args) >= 2:
        job_name = args[1]
    # log.info('args type: %s, args: %s' % (type(args), args))
    start_update_room_job(job_name)
