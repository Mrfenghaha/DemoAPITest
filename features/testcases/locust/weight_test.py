# -*- coding: utf-8 -
from locust import HttpLocust, task
from common.runMain import RunLocust
from common.readConfig import *
from features.apis import mockServerConfigsInfo_api, mockServerMockShowLists_api


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task
    def test_demo_get(self):
        self.runLocust(mockServerConfigsInfo_api.configs_info())


class TestLocust2(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task
    def test_demo_post(self):
        page_num, num = 10, 1
        self.runLocust(mockServerMockShowLists_api.mock_show_lists(page_num, num))


class QueryOne(HttpLocust):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000
    weight = 1
    host = host


class QueryTwo(HttpLocust):
    task_set = TestLocust2
    min_wait = 1000
    max_wait = 3000
    weight = 2
    host = host
