# -*- coding: utf-8 -
import re
import yaml
from common import*


class ReadConfigFile:
    def __init__(self, path):
        self.path = path

    def read_yaml_file(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            # 使用load方法将读出的字符串转字典
            content = yaml.full_load(file)
            file.close()
        return content


email_info = ReadConfigFile(email_yaml_path).read_yaml_file()
env_info = ReadConfigFile(env_yaml_path).read_yaml_file()

# 邮箱信息
email_info = email_info['email_info']

# host地址
host = env_info['host']
# mysql信息
mysql_info = env_info['mysql_info']
# mongodb信息
mongodb_info = env_info['mongodb_info']
