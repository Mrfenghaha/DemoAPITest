# -*- coding: utf-8 -
import os
import re

cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(cur_path, 'config')
env_info_path = os.path.join(config_path, 'env.yaml')
env_path = os.path.join(config_path, 'envConfig')


def get_env_list():
    env_list = []
    lst = os.listdir(env_path)
    for c in lst:
        if os.path.splitext(c)[1] == '.yaml':
            env = "".join(re.findall(r"env(.+?).yaml", c))
            env_list.append(env)
    return env_list


def env_specify(env):
    lst = get_env_list()
    if env in lst:
        env_info = os.path.join(env_path, "env" + env + ".yaml")
        file = open(env_info, 'r', encoding='utf-8').read()
        with open(env_info_path, 'w', encoding='utf-8') as env_file:
            env_file.write(file)
        env_file.close()
    else:
        print("环境参数错误，请输入" + str(lst) + "中的一种")
        quit()
