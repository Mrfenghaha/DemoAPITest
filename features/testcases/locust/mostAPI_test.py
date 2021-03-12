# -*- coding: utf-8 -
from locust import HttpUser, task
from common.runMain import RunLocust
from common import *
from features.apis import mockServerGetConfigs_api, mockServerGetMockList_api


class TestLocust(RunLocust):

    def on_start(self):
        print('开始性能测试')
        # self.logger = LocustLogger()
        # self.logger.get_locust_Hook()

    @task
    def test_demo_post(self):
        parm = {"page": 1, "size": 10}
        self.runLocust(name='tool/mock_server/get_mock_list', parm=parm)
        self.runLocust(mockServerGetConfigs_api.get_configs())
        # self.logger.get_requests_log(method='GET', path='/', requests={}, response=resp.json())


class Query(HttpUser):
    task_set = TestLocust
    min_wait = 1000
    max_wait = 3000

    host = host
