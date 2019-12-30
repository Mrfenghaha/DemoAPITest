# -*- coding: utf-8 -
import os
import sys
import time
import unittest
from common.HTMLTestRunner import HTMLTestRunner
from common.emailSend import email_send
from common.envSpecify import env_specify
# from tomorrow import threads


# 当前脚本所在的文件绝对路径
cur_path = os.path.dirname(os.path.realpath(__file__))
res_path = os.path.join(cur_path, "result")


# 将当前路径设置为python的临时环境变量，用于命令执行
# 需要设置是因为项目存在多处相互调用
# os.putenv("PYTHONPATH", cur_path)


def add_api(suite, name):
    # 指定测试目录
    case_path = os.path.join(cur_path, "tests/testcase/" + suite)
    if name == 'all':
        # 定义测试目录为指定目录
        discover = unittest.defaultTestLoader.discover(case_path, pattern="*.py", top_level_dir=None)
        return discover
    else:
        # 定义测试目录为指定目录
        discover = unittest.defaultTestLoader.discover(case_path, pattern=name + ".py", top_level_dir=None)
        return discover


# 根据情况选择是否多线程进行，较少时单线程反而更快
# @threads(3)
def run_api(all_api):

    # 指定报告存储位置以及报告名称
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    report_path = os.path.join(res_path, "reports")
    # 如果没有reports文件就创建一个文件
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    report_abspath = os.path.join(report_path, now+".html")
    print("报告地址:%s" % report_abspath)

    # 执行所有用例，并将结果写入HTML测试报告中
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况')
    runner.run(all_api)
    fp.close()


if __name__ == "__main__":
    env = sys.argv[1]
    suite = sys.argv[2]
    name = sys.argv[3]
    env_specify(env)
    all_api = add_api(suite, name)
    run_api(all_api)
    email_send()
