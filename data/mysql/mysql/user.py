# -*- coding: utf-8 -
from common.readConfig import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()


'''
codes验证码
'''


class Codes(Base):
    # 表的名字:
    __tablename__ = 'codes'
    # 表的结构:
    id = Column(String(100), primary_key=True)
    phone = Column(String(100))
    code = Column(String(100))


class UserUtil:

    def __init__(self):
        engine = create_engine(mysql + "/user")
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_code(self, condition, *param):
        if condition == 'phone':
            phone = param[0]
            t = self.session.query(Codes).filter(Codes.phone == phone).order_by(Codes.id.desc()).first()
            self.session.close()
            return t
        else:
            print('方法不存在请补充')
