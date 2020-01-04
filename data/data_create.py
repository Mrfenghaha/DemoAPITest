# -*- coding: utf-8 -
import pytz
import time
import datetime
from data.dataCreate import custom


class DataCreate:

    def data_create(self):
        a = {
            "now_time": datetime.datetime.now(),  # 当前时间
            "now_time_stamp": round(time.time() * 1000),  # 当前13位时间戳
            "now_time_iso": datetime.datetime.now(pytz.timezone('PRC')).isoformat(),  # 北京时间utc的iso格式
            "phone": str(round(time.time() * 1000))[4:13],  # 由时间戳号生成的手机
            "password": "password"
        }

        return a

    def custom(self):
        return custom.custom()


if __name__ == "__main__":
    DataCreate().data_create()
