# -*- coding: utf-8 -
import unittest
from common.runMain import SendRequest


class Suite(SendRequest):
    def suite(self):
        page, size = self.data['page'], self.data['size']

        # 发起登录
        parm = {"page": page, "size": size}
        result = self.sendRequest(name="tool/mock_server/get_mock_list", parm=parm)
        return result
