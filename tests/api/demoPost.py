# -*- coding: utf-8 -
from config.readConfig import *
from common.runMain import RunMain


def demo_post(phone, password):
    # account：手机号
    # password：密码

    url = host + '/api/login'
    method = 'post'
    headers = {'content-type': 'application/json'}
    data = {'account': phone, 'password': password}

    result = RunMain(method, url, headers, data).run_main()
    return result
