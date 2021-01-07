# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest
from data.dataCreate import DataCreate


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """正常数据"""
        data = DataCreate().data_create()
        # 准备数据
        page, size = data['page'], data['size']
        result = self.sendRequest("mock_server_get_mock_list", {"page": page, "size": size})
        self.assertEqual(result['code'], 200)
        self.assertEqual(result['body']["success"], True)

    def test_case02(self):
        """异常数据-空"""
        data = DataCreate().data_create()
        # 准备数据
        size = data['size']
        result = self.sendRequest("mock_server_get_mock_list", {"size": size})
        self.assertEqual(result['body']["success"], False)
        self.assertEqual(result['body']["error_message"], "param is error, param not filled or type error")

    def test_case03(self):
        """异常数据-null"""
        data = DataCreate().data_create()
        # 准备数据
        page, size = None, data['size']
        result = self.sendRequest("mock_server_get_mock_list", {"page": page, "size": size})
        self.assertEqual(result['body']["success"], False)
        self.assertEqual(result['body']["error_message"], "param is error, param not filled or type error")

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
