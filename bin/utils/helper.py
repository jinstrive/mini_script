# coding: utf-8
import datetime
import json
import os
from pathlib import Path


def timetostr(dtime):
    # 导入datetime模块
    # print(dtime)

    # 获取当前时间的时分秒
    hour = dtime.hour
    minute = dtime.minute
    second = dtime.second
    # 格式化成字符串，例如"14:03:38"
    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

    # 打印结果
    # print(time_str)
    return time_str

def get_current_date():
    return datetime.date.today().strftime("%Y-%m-%d")


def get_timestr_from_period_id(period_id):
    start = datetime.datetime(2023, 2, 21, 0, 0, 0)
    end = start + datetime.timedelta(days=1)
    interval = (end - start) / 48
    
    start_dt = start + period_id * interval
    end_dt = start + (period_id+1) * interval
    
    start_time = start_dt.time().strftime("%H:%M:%S")
    end_time = end_dt.time().strftime("%H:%M:%S")
    return start_time, end_time



def get_date_period_id(time_str):
    """
    根据时间字符串，获取所属的时段id
    """

    # 创建一个日期对象，表示今日日期
    date_obj = datetime.date.today()
    # 使用strptime()函数将字符串转换成时间对象
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    # 使用combine()方法将日期对象和时间对象组合成一个日期时间对象
    datetime_obj = datetime.datetime.combine(date_obj, time_obj)
    # 创建一个今日凌晨的日期时间对象
    midnight_obj = datetime.datetime.combine(date_obj, datetime.time.min)
    # 计算两个日期时间对象之间的时间差，得到一个timedelta对象
    delta = datetime_obj - midnight_obj
    # 获取timedelta对象的总秒数，并除以60得到总分钟数
    minutes = delta.total_seconds() / 60
    period_id = int(minutes / 30)
    # print(minutes, period_id)
    return period_id

def get_now_period_id():
    """
    根据时间字符串，获取所属的时段id
    """

    # 创建一个日期对象，表示今日日期
    date_obj = datetime.date.today()
    # 使用strptime()函数将字符串转换成时间对象
    time_obj = datetime.datetime.now().time()
    # 使用combine()方法将日期对象和时间对象组合成一个日期时间对象
    datetime_obj = datetime.datetime.combine(date_obj, time_obj)
    # 创建一个今日凌晨的日期时间对象
    midnight_obj = datetime.datetime.combine(date_obj, datetime.time.min)
    # 计算两个日期时间对象之间的时间差，得到一个timedelta对象
    delta = datetime_obj - midnight_obj
    # 获取timedelta对象的总秒数，并除以60得到总分钟数
    minutes = delta.total_seconds() / 60
    period_id = int(minutes / 30)
    # print(minutes, period_id)
    return period_id


# # 定义一个异步函数，用于写入文件
# async def write_file(text, filename):
#     # 使用aiofiles.open函数打开文件，使用异步上下文管理器
#     async with aiofiles.open(filename, 'w') as f:
#         # 使用await关键字等待文件写入操作完成
#         await f.write(text)

# # 定义一个主函数，用于调用写入文件的函数
# async def main():
#     # 定义要写入的文本内容
#     text = "hey"
#     # 定义要写入的文件名
#     filename = "test.txt"
#     # 调用写入文件的函数，并使用await关键字等待其完成
#     await write_file(text, filename)
#     # 打印提示信息
#     print(f"Write {text} to {filename} successfully")

# # 使用asyncio.run函数运行主函数
# asyncio.run(main())


def get_json_from_resource_file(filename):
    # 从resource文件夹中加载json数据
    # json_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/resource/%s.json' % filename
    f_name = "%s.json" % filename
    json_path = Path(__file__).parent.parent / "resource" / f_name
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 定义一个函数，将秒数转换为时分秒的格式
def format_time(seconds):
  # 将秒数除以 60，得到分钟数和剩余的秒数
  minutes, seconds = divmod(seconds, 60)
  # 将分钟数除以 60，得到小时数和剩余的分钟数
  hours, minutes = divmod(minutes, 60)
  # 将小时数、分钟数和秒数拼接成一个字符串
  return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"