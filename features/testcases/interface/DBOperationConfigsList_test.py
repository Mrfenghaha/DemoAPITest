# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试1"""
        parm = {"page": 1, "size": 10}
        check = [{"code": ("=", 200)}]
        self.sendRequest("db_operation_get_configs_list", parm, check)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
