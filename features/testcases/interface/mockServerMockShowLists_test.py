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
        # 准备数据
        parm = {"page": 1, "size": 10}
        check = [{'code': ('=', 200)}, {'body/success': ('=', True)}]
        self.sendRequest("mock_server_get_mock_list", parm, check)

    def test_case02(self):
        """异常数据-空"""
        # 准备数据
        parm = {"size": 10}
        check = [{'code': ('=', 403)}, {'body/success': ('=', False)},
                 {'body/error_message': ('assertEqual', "param is error, param not filled or type error")}]
        self.sendRequest("mock_server_get_mock_list", parm, check)

    def test_case03(self):
        """异常数据-null"""
        # 准备数据
        parm = {"page": None, "size": 10}
        check = [{'code': ('=', 403)}, {'body/success': ('=', False)},
                 {'body/error_message': ('assertEqual', "param is error, param not filled or type error")}]
        self.sendRequest("mock_server_get_mock_list", parm, check)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
