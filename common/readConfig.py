# -*- coding: utf-8 -
import os
import yaml


# 人称最稳重方法，每加一层os.path.dirname()即向上翻一层,os.getcwd()获取当前目录的绝对路径
# os.getcwd()用于获取执行py文件的位置，例如在根目录执行获取的位置就是根目录，在common下执行就是common路径
# os.path.dirname(os.path.realpath(__file__))是获取包含该执行语句的py文件的绝对路径
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(cur_path, 'config')
env_info_path = os.path.join(config_path, 'env.yaml')
email_info_path = os.path.join(config_path, 'email.yaml')

# 如果没有config,自动创建
if not os.path.exists(config_path):
    os.mkdir(config_path)  # 创建config文件夹

# 如果没有config/email.yaml,自动创建并写入默认值
if not os.path.exists(email_info_path):
    with open(email_info_path, 'w', encoding='utf-8') as file:
        file.write("# 邮箱配置\nemail_info:\n"
                   "  server: xxx.xxx.xxx\n"
                   "  sender: xxx@xxxxxx.com\n"
                   "  password: xxxxxx\n"
                   "  receiver: ['xxx@xxxxxx.com','xxx@xxxxxx.com']")
    file.close()


with open(email_info_path, 'r', encoding='utf-8') as file:
    # 使用load方法将读出的字符串转字典
    email_info = yaml.full_load(file)
    file.close()

email_info = email_info['email_info']

# 如果没有config/env.yaml,自动创建并写入默认值
if not os.path.exists(env_info_path):
    with open(env_info_path, 'w', encoding='utf-8') as file:
        file.write('# host环境IP\nhost: http://xxx.xx.x.xx\n'
                   '# mysql服务信息\nmysql_info:\n  ip:xxxx\n  port: 3306\n  account: xxxx\n  password: xxxx\n'
                   '# mongodb服务信息\nmongodb_info:\n  ip:xxxx\n  port: 3306\n  account: xxxx\n  password: xxxx\n')
    file.close()


with open(env_info_path, 'r', encoding='utf-8') as file:
    # 使用load方法将读出的字符串转字典
    env_info = yaml.full_load(file)
    file.close()
# host地址
host = env_info['host']
# mysql信息
mysql_info = env_info['mysql_info']
# mongodb信息
mongodb_info = env_info['mongodb_info']
