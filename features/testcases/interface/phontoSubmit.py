# -*- coding: utf-8 -
import unittest
from common import *
from common.runMain import SendRequest


class Test(SendRequest):

    def setUp(self):
        print('-----start-----')

    # unittest执行测试必须以test开头
    def test_case01(self):
        """测试1"""
        parm = {"body/upload": ("image.png", open(os.path.join(cur_path, "docs", "file.png"), "rb").read(), "multipart/form-data")}
        self.sendRequest(mode='uploadFile', name="phoneSubmit", parm=parm)

    def tearDown(self):
        print('-----end-----')


if __name__ == "__main__":
    unittest.main()
