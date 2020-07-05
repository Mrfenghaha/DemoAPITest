# -*- coding: utf-8 -
import gevent.monkey
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决
import time
import unittest
from common import *
from common.run.htmlTestRunner import HTMLTestRunner
from common.run.BeautifulReport import BeautifulReport
from tomorrow import threads


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

    def run_case(self):
        # 指定报告存储位置以及报告名称
        now = time.strftime("%Y-%m-%d-%H-%M-%S")
        report_abspath = os.path.join(reports_path, now + ".html")
        print("报告地址:file://%s" % report_abspath)

        # 执行所有用例，并将结果写入HTML测试报告中
        fp = open(report_abspath, "wb")
        runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况')
        runner.run(self.add_case())
        fp.close()

    # 实现多线程执行，但每一个py文件会生成一个报告文件，不利于查找出错内容，并且也会出现部分log错乱的问题
    @threads(5)
    def threads_run(self, report_path, cases):
        # 指定报告存储位置以及报告名称
        now = time.strftime("%M-%S")
        report_abspath = os.path.join(report_path, now + ".html")  # 本次执行所有报告以时间（分-秒）.html

        # 执行所有用例，并将结果写入HTML测试报告中
        fp = open(report_abspath, "wb")
        runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况')
        runner.run(cases)
        fp.close()

    def threads_run_case(self):
        now = time.strftime("%Y-%m-%d-%H-%M")
        report_path = os.path.join(reports_path, now)  # 为了便于区分报告，根据开始时间（到分）创建文件夹
        if not os.path.exists(report_path):
            os.mkdir(report_path)
        print("报告地址:file://%s" % report_path)
        cases = self.add_case()
        for case in cases:
            self.threads_run(report_path, case)

    # 使用外部报告BeautifulReport实现多线程执行，但报告有问题（仅能记录成功/失败，log内容会错乱）
    # 会返回3个报告地址，已最后一个为准
    @threads(5)
    def new_threads_run(self, case):
        # 指定报告存储位置以及报告名称
        now = time.strftime("%Y-%m-%d-%H-%M-%S")
        result = BeautifulReport(case)
        result.report(filename=now, description='API自动化测试报告', log_path=reports_path)

    def new_threads_run_case(self):
        cases = self.add_case()
        for case in cases:
            self.new_threads_run(case)
