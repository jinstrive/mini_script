# -*- coding: utf-8 -*-
import os
import json
from settings import log
from utils.constants import *
from settings import SQLITE_URL, SQLITE_TEST_URL
import sqlite3
from pathlib import Path



def get_json_from_resource_file(filename):
    # 从resource中加载json数据
    # json_path = os.path.dirname(os.path.abspath(__file__)) + '/resource/%s.json' % filename
    f_name = "%s.json" % filename
    json_path = Path(__file__).parent / "resource" / f_name
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def init_maheyou_store():
    maheyou_dict = XCX_BRANDS.get('maheyou')
    # 初始化麻合友的店铺信息, 房间信息在获取占用时更新
    json_stores = get_json_from_resource_file('maheyou_allshop_withstatus')
    json_citys = get_json_from_resource_file('maheyou_citys')
    citys_dict = dict(map(lambda d: (str(d["city_code"]), d), json_citys['result']['city']))
    store_arr = json_stores['result']['list']
    # print(store_arr[0])
    # print(citys_dict.popitem())
    # 将测试数据库初始化
    conn = sqlite3.connect(SQLITE_TEST_URL)
    # conn = sqlite3.connect(SQLITE_TEST_URL)
    cur = conn.cursor()
    # try:
    for store in store_arr:
        store_ref_id = store['sid']
        cur.execute(SQL_FIND_STORE_ID % (maheyou_dict['brand_id'], store_ref_id))
        exist_store = cur.fetchone()

        # 如果已存在，则不执行
        if exist_store:
            continue

        new_store_dict = maheyou_dict.copy()
        new_store_dict['store_ref_id'] = store_ref_id
        new_store_dict['store_name'] = store['name']

        # 获取店铺所在的省份
        province = citys_dict.get(str(store['city_code']))
        city = citys_dict.get(str(store['city_code']))
        # new_store_dict['province'] = citys_dict.get(str(store['city_code']))['province']
        # new_store_dict['city'] = citys_dict.get(str(store['city_code']))['name']
        new_store_dict['province'] = province.get('province') if province else ''
        new_store_dict['city'] = city.get('name') if city else ''
        new_store_dict['store_address'] = store['address']
        new_store_dict['tel'] = store.get('telephone') if store.get('telephone') else ''
        new_store_dict['lat'] = store.get('lat') if store.get('lat') else ''
        new_store_dict['lng'] = store.get('lng') if store.get('lng') else ''

        # print(new_store_dict)

        # 插入店铺数据
        cur.execute(SQL_INSERT_STORE, new_store_dict)
        conn.commit()
    # except Exception as e:
    #     log.error(e)

    cur.close()
    conn.close()



if __name__ == '__main__':
    print(get_json_from_resource_file('maheyou_all_shop'))
    # init_maheyou_store()
    # print(get_json_from_resource_file('heyyiou'))
    # f_name = "%s.json" % 'filefff'
    # json_path = Path(__file__).parent / "resource" / f_name
    # print(json_path)
    