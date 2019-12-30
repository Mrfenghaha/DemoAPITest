# -*- coding: utf-8 -
from config.readConfig import *
from common.runMain import RunMain


def demo_get():

    url = 'https://www.csdn.net/'
    method = 'get'
    headers = {}
    data = {}

    result = RunMain(method, url, headers, data).run_main()
    return result


