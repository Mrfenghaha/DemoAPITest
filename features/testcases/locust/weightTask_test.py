# -*- coding: utf-8 -
from locust import HttpLocust, task
from common.runMain import RunLocust
from common import *
from features.apis import mockServerGetConfigs_api, mockServerGetMockList_api, dbOperationGetConfigList_api,\
    dbOperationGetOperationList_api


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task(3)
    def test_configs_info(self):
        self.runLocust(mockServerGetConfigs_api.configs_info())

    @task
    def test_mock_show_lists(self):
        page_num, num = 10, 1
        self.runLocust(mockServerGetMockList_api.mock_show_lists(page_num, num))


class TestLocust2(RunLocust):

    def on_start(self):
        print('开始性能测试')

    @task(5)
    def test_configs_show_lists(self):
        page_num, num = 10, 1
        self.runLocust(dbOperationGetConfigList_api.configs_show_lists(page_num, num))

    @task
    def test_operations_show_lists(self):
        page_num, num = 10, 1
        self.runLocust(dbOperationGetOperationList_api.operations_show_lists(page_num, num))


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
    weight = 4
    host = host
