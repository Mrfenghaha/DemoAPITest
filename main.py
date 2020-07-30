# -*- coding: utf-8 -
import time
import argparse
from common.run.envSpecify import EnvSpecify


parser = argparse.ArgumentParser()
parser.add_argument('--env', '-e', help='环境变量参数，非必要参数')
parser.add_argument('--collection', '-c', help='测试用例集合名称，非必要参数(testcases中用于划分用例集合的文件夹名,当未划分用例集合时不需要)')
parser.add_argument('--name', '-n', help='测试用例名称，必要参数', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    EnvSpecify().specify(args.env)
    time.sleep(2)
    # 因为specify修改了env配置文件，需要重新加载common模块，读取环境变量
    import common
    from importlib import reload

    reload(common)
    # 重新加载更新环境变量后，再次调用RunCase类
    from common.run.runCase import RunCase

    RunCase(args.collection, args.name).run_case()
    # from common.run.emailSend import EmailSend
    # EmailSend().email_send()
