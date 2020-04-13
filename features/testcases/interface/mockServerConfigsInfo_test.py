# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest
from features.apis import mockServerConfigsInfo_api


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试登录1"""
        result = self.sendRequest(mockServerConfigsInfo_api.configs_info())
        self.assertEqual(result.status_code, 200)

    def test_case02(self):
        """测试登录2"""
        result = self.sendRequest(mockServerConfigsInfo_api.configs_info())
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
