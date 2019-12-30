# -*- coding: utf-8 -
from tests.api import demoPost


def suite_post(data):
    phone = data['phone']
    password = data['password']

    # 发起登录
    login = demoPost.demo_post(phone, password)
    return login
