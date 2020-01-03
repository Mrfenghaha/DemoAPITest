# -*- coding: utf-8 -
from config.readConfig import *


def demo_post(phone, password):
    # account：手机号
    # password：密码

    request = {
        "url": host + '/api/login',
        "method": 'post',
        "headers": {'content-type': 'application/json'},
        "data": {'account': phone, 'password': password}
    }

    return request
