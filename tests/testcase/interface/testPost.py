# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest
from data.data_create import DataCreate
from tests.api import demoPost


class Test(unittest.TestCase, SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """正常数据-密码登录-登陆成功"""
        data = DataCreate().data_create()
        # 准备数据
        phone = data['phone']
        password = '123456'
        result = self.sendRequest(demoPost.demo_post(phone, password))
        self.assertEqual(result.json()["success"], True)

    def test_case02(self):
        """异常数据-手机号码为空-登陆失败"""
        data = Data().data_create()
        # 准备数据
        phone = ''
        password = data['password']
        result = self.sendRequest(demoPost.demo_post(phone, password))
        self.assertEqual(result.json()["success"], False)
        self.assertEqual(result.json()["err_msg"], 'params validate error')

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
