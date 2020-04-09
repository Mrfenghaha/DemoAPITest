# -*- coding: utf-8 -
from locust import HttpLocust, task
from common.runMain import RunLocust
from common.readConfig import *
from features.apis import mockServerConfigsInfo, mockServerMockShowLists


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task(2)
    def test_demo_post(self):
        page_num, num = 10, 1
        self.runLocust(mockServerMockShowLists.mock_show_lists(page_num, num))

    @task(1)
    def test_demo_get(self):
        self.runLocust(mockServerConfigsInfo.configs_info())


class Query(HttpLocust):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000
    host = host
