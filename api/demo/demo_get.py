# -*- coding: utf-8 -
from common.readConfig import *
from common.runMain import RunMain


class DemoGet:

    def demo_get(self):

        url = 'https://www.csdn.net/'
        method = 'get'
        headers = {}
        data = {}

        result = RunMain(method, url, headers, data).run_main()
        return result

