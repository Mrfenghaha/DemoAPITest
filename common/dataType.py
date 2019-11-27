# -*- coding: utf-8 -
from decimal import *


# string类型转布尔值类型
def str_to_boolean(value):
    return value == 'true'


# string类型转int字符类型
def str_to_int(value):
    return int(value)


# int类型转string字符类型
def int_to_str(value):
    return str(value)


# 浮点数转为str字符类型
def decimal_to_int(value):
    return int(Decimal(value).quantize(Decimal('0')))
