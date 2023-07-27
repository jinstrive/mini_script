#-*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import socket
from utils.logger import initlog
# ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# OPENAPI_PATH = os.path.dirname(ROOT_PATH)
# GRAY_VERSION = os.path.basename(ROOT_PATH)
# log = initlog({
#     'INFO': '%s/log/%s.log' % (ROOT_PATH, GRAY_VERSION),
#     'NOTE': '%s/log/%s.log' % (ROOT_PATH, GRAY_VERSION),
#     'WARN': '%s/log/%s.log' % (ROOT_PATH, GRAY_VERSION),
#     'ERROR': '%s/log/%s.log' % (ROOT_PATH, GRAY_VERSION),
# }, backup_count=0, console=True)

project_root = Path(__file__).parent.parent
log_file_name = "%s.log" % project_root.name
log_path = project_root / "log" / log_file_name

log = initlog({
    'INFO': log_path,
    'NOTE': log_path,
    'WARN': log_path,
    'ERROR': log_path,
}, backup_count=0, console=True)



SQLITE_URL = Path(__file__).parent.parent / "mahjong.db"
SQLITE_TEST_URL = Path(__file__).parent.parent / "mahjong_test.db"


MAHEYOU_COOKIE = "auth_user=3507875%7C18969040499%7Ce69a8c6e8b6199296f9c912fdeb4c4e2%7C1690212125%7C2883278%7C3046600; expires=Sat, 24-Jul-2023 15:22:05 UTC; Max-Age=86400"
MAHEYOU_TIMESTAMP_PRIVATE = "1690350117288"
                        
                        

if __name__ == '__main__':
    
    # test_select_sqlite()
    # print(ROOT_PATH)
    # print(OPENAPI_PATH)
    # print(GRAY_VERSION)
    log.info('log success!')
    log.error('error success!')

