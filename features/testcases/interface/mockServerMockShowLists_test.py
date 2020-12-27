# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest
from data.dataCreate import DataCreate
from features.apis import mockServerGetMockList_api


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """正常数据-密码登录-登陆成功"""
        data = DataCreate().data_create()
        # 准备数据
        page, size = data['page'], data['size']
        result = self.sendRequest(mockServerGetMockList_api.mock_show_lists(page, size))
        self.assertEqual(result.json()["success"], True)

    def test_case02(self):
        """异常数据-手机号码为空-登陆失败"""
        data = DataCreate().data_create()
        # 准备数据
        page, size = "", data['size']
        result = self.sendRequest(mockServerGetMockList_api.mock_show_lists(page, size))
        self.assertEqual(result.json()["success"], False)
        self.assertEqual(result.json()["error_message"], "param is error, param not filled or type error")

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
