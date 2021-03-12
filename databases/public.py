# -*- coding: utf-8 -
import pymysql
import pymongo
from urllib import parse
from common import *
mysql_info = env['mysql_info']
mongodb_info = env['mongodb_info']


def execute_mysql(sql):
    db = pymysql.connect(host=mysql_info['ip'], port=mysql_info['port'], user=mysql_info['mysql_account'],
                         password=mysql_info['password'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return cursor


def client_mongodb(database):
    account = parse.quote_plus(mongodb_info['account'])
    password = parse.quote_plus(mongodb_info['password'])
    mongodb = "mongodb://%s:%s@%s:%s/%s" % (account, password, mongodb_info['ip'], mongodb_info['port'], database)
    client = pymongo.MongoClient(mongodb)
    return client
