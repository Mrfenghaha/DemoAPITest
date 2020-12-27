# -*- coding: utf-8 -
from locust import HttpUser, task
from common.runMain import RunLocust
from common import *
from features.apis import mockServerGetConfigs_api, mockServerGetMockList_api


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task(2)
    def test_demo_post(self):
        page_num, num = 10, 1
        self.runLocust(mockServerGetMockList_api.get_mock_list(page_num, num))

    @task(1)
    def test_demo_get(self):
        self.runLocust(mockServerGetConfigs_api.get_configs())


class Query(HttpUser):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000
    host = host
