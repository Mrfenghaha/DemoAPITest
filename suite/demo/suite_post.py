# -*- coding: utf-8 -
from api.demo.demo_post import DemoPost


def suite_post(data):
    phone = data['phone']
    password = data['password']

    # 发起登录
    login = DemoPost().demo_post(phone, password)
    return login
