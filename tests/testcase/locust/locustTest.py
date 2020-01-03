# -*- coding: utf-8 -
from locust import HttpLocust, task
from common.runMain import RunMain
from config.readConfig import *
from tests.api import demoGet, demoPost


class TestLocust(RunMain):

    def on_start(self):
        print('开始性能测试')

    @task
    def test_locust(self):
        phone = "1234567890"
        password = "password"
        self.runLocust(demoGet.demo_get())
        self.runLocust(demoPost.demo_post(phone, password))


class Query(HttpLocust):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000
    host = host
