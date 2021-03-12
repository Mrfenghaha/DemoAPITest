# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Test(SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试1"""
        parm = {"page": 1, "size": 10}
        self.sendRequest(name="tool/db_operation/get_config_list", parm=parm, check_code=200)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
