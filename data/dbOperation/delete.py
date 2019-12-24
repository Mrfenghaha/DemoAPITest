# -*- coding: utf-8 -
from data.dbOperation.public import *


'''
codes验证码
'''


def delete(id):
    sql = "delete from xxx.xxx where id = '%s'" % id
    execute_mysql(sql)
