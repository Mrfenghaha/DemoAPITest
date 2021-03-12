# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Test(SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试1"""
        parm = {"token": '', "sid": ''}
        self.sendRequest(mode='websocket', name="websocket", parm=parm)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
