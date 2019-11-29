# -*- coding: utf-8 -
import os
import yaml


# 人称最稳重方法，每加一层os.path.dirname()即向上翻一层,os.getcwd()获取当前目录的绝对路径
# os.getcwd()用于获取执行py文件的位置，例如在根目录执行获取的位置就是根目录，在common下执行就是common路径
# os.path.dirname(os.path.realpath(__file__))是获取包含该执行语句的py文件的绝对路径
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(cur_path, 'config')
env_path = os.path.join(config_path, 'env.yaml')
email_path = os.path.join(config_path, 'email.yaml')

# 如果没有config,自动创建
if not os.path.exists(config_path):
    os.mkdir(config_path)  # 创建config文件夹

# 如果没有config/email.yaml,自动创建并写入默认值
if not os.path.exists(email_path):
    os.mknod(email_path)  # 创建email.yaml文件
    with open(email_path, 'w') as file:
        file.write("# 邮箱配置\n"
                   "server: xxx.xxx.xxx\n"
                   "sender: xxx@xxxxxx.com\n"
                   "password: xxxxxx\n"
                   "receiver: ['xxx@xxxxxx.com','xxx@xxxxxx.com']")


with open(email_path, 'r', encoding='utf-8') as file:
    # 使用load方法将读出的字符串转字典
    email_info = yaml.full_load(file)

email_server = email_info['server']

email_sender = email_info['sender']

email_password = email_info['password']

email_receiver = email_info['receiver']

# 如果没有config/env.yaml,自动创建并写入默认值
if not os.path.exists(env_path):
    os.mknod(env_path)  # 创建env.yaml文件
    with open(env_path, 'w') as file:
        file.write("host: http://xxx.xx.x.xx\n"
                   "mysql_address: mysql+pymysql://xxx(帐号):xxx(密码)@xxx.xx.x.xx(IP地址):3306")


with open(env_path, 'r', encoding='utf-8') as file:
    # 使用load方法将读出的字符串转字典
    env_info = yaml.full_load(file)

host = env_info['host']

mysql = env_info['mysql_address']
