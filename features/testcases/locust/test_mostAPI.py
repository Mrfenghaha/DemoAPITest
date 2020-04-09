# -*- coding: utf-8 -
from locust import HttpLocust, task
from common.runMain import RunLocust
from common.readConfig import *
from features.apis import mockServerConfigsInfo, mockServerMockShowLists


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')
        # self.logger = LocustLogger()
        # self.logger.get_locust_Hook()

    @task
    def test_demo_post(self):
        page_num, num = 10, 1
        self.runLocust(mockServerMockShowLists.mock_show_lists(page_num, num))
        self.runLocust(mockServerConfigsInfo.configs_info())
        # self.logger.get_requests_log(method='GET', path='/', requests={}, response=resp.json())


class Query(HttpLocust):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000

    host = host
