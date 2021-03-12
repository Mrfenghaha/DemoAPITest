# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Test(SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """正常数据"""
        # 准备数据
        parm = {"page": 1, "size": 10}
        check = {'success': ('=', True)}
        self.sendRequest(name="tool/mock_server/get_mock_list", parm=parm, check_code=200, check_body=check)

    def test_case02(self):
        """异常数据-空"""
        # 准备数据
        parm = {"size": 10}
        check = {'success': ('=', False),
                 'error_message': ('=', "param is error, param not filled or type error")}
        self.sendRequest(name="tool/mock_server/get_mock_list", parm=parm, check_code=403, check_body=check)

    def test_case03(self):
        """异常数据-null"""
        # 准备数据
        parm = {"page": None, "size": 10}
        check = {'success': ('=', False),
                 'error_message': ('=', "param is error, param not filled or type error")}
        self.sendRequest(name="tool/mock_server/get_mock_list", parm=parm,check_code=403, check_body=check)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
