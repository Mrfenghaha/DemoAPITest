# -*- coding: utf-8 -
from locust import HttpUser, TaskSet, task


# 定义用户行为，继承TaskSet类，用于描述用户行为
class UserBehavior(TaskSet):

    # 装饰该方法为一个事务
    @task
    # 表示一个用户行为
    def baidu_index(self):
        self.client.get("/")


class WebsiteUser(HttpUser):
    # 指向一个定义的用户行为类
    task_set = UserBehavior
    # 执行事务之间用户等待时间的下界（单位：毫秒）
    min_wait = 3000
    # 执行事务之间用户等待时间的上界（单位：毫秒）
    max_wait = 6000
    # 设置 Locust 多少秒后超时，如果为 None ,则不会超时。
    stop_timeout = 5


'''
locust -f features/locust/sample1.py --host=https://www.baidu.com
-f 指定性能测试脚本文件。
--host 指定被测试应用的URL的地址，注意访问百度使用的HTTPS协议。

locust -f features/locust/sample1.py --host=https://www.baidu.com --no-web -c 10 -r 2 -t 1m
--no-web 表示不使用Web界面运行测试。
-c 设置虚拟用户数。
-r 设置每秒启动虚拟用户数。
-t 设置设置运行时间。
'''