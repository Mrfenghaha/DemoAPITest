# -*- coding: utf-8 -
from config.readConfig import *
from common.runMain import RunMain


def demo_get():

    request = {
        "url": 'https://www.csdn.net/',
        "method": 'get',
        "headers": {},
        "data": {}
    }

    return request


