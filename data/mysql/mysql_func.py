# -*- coding: utf-8 -
import datetime
from data.mysql.mysql import *


'''
以下内容适用于用户phl_user_prod
'''
User = user.UserUtil()


def get_user(table, condition, *param):
    if table == 'codes':
        data = User.get_code(condition, *param)
        return data
    else:
        print('表不存在请补充')
