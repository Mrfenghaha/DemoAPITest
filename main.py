# -*- coding: utf-8 -
import argparse
from runcase.envSpecify import EnvSpecify
from runcase.emailSend import EmailSend
from runcase.runcase import RunCase


parser = argparse.ArgumentParser()
parser.add_argument('--env', '-e', help='环境变量参数，非必要参数')
parser.add_argument('--collection', '-c', help='测试用例集合名称，非必要参数(testcases中用于划分用例集合的文件夹名,当未划分用例集合时不需要)')
parser.add_argument('--name', '-n', help='测试用例名称，必要参数', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    EnvSpecify().specify(args.env)
    RunCase(args.collection, args.name).run_case()
    # EmailSend().email_send()
