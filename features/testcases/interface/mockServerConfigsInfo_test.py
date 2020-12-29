# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试1"""
        result = self.sendRequest("mock_server_get_configs", {})
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
