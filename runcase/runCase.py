# -*- coding: utf-8 -
import time
import unittest
from common import *
from runcase.htmlTestRunner import HTMLTestRunner
# from tomorrow import threads


class RunCase:
    def __init__(self, suite, name):
        self.suite = suite
        self.name = name

    def add_case(self):
        # 指定测试目录
        if self.suite is None:
            case_path = os.path.join(cur_path, "features/testcases/")
        else:
            case_path = os.path.join(cur_path, "features/testcases/" + self.suite)
        if self.name == 'all':
            # 定义测试目录为指定目录
            discover = unittest.defaultTestLoader.discover(case_path, pattern="*.py", top_level_dir=None)
            return discover
        else:
            # 定义测试目录为指定目录
            discover = unittest.defaultTestLoader.discover(case_path, pattern=self.name + ".py", top_level_dir=None)
            return discover

    # 根据情况选择是否多线程进行，较少时单线程反而更快
    # @threads(3)
    def run_case(self):
        # 指定报告存储位置以及报告名称
        now = time.strftime("%Y-%m-%d-%H-%M-%S")
        report_abspath = os.path.join(reports_path, now+".html")
        print("报告地址:%s" % report_abspath)

        # 执行所有用例，并将结果写入HTML测试报告中
        fp = open(report_abspath, "wb")
        runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况')
        runner.run(self.add_case())
        fp.close()
