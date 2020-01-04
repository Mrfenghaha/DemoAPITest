# -*- coding: utf-8 -


def demo_post(phone, password):
    # account：手机号
    # password：密码

    request = {
        "url": '/api/login',
        "method": 'post',
        "headers": {'content-type': 'application/json'},
        "data": {'account': phone, 'password': password}
    }

    return request
