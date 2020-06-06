# -*- coding: utf-8 -
import os
import logging
from locust import events
from logging.handlers import RotatingFileHandler


class LocustLogger:
    """日志记录"""

    def __init__(self, path, name):
        self.filePath = path  # 存放文件的路径
        self.fileName = name  # 存放文件的名字
        # self.BACK_UP_COUNT = 5000                    # 文件分割上限数
        # self.MAX_LOG_BYTES = 1024 * 1024 * 3        # 单个文件最大记录数10M
        self.create_handler()  # 初始化创建日志handler
        self.create_logger()  # 初始化创建Logger

    def create_handler(self):
        """建立handler"""
        self.handler = RotatingFileHandler(filename=os.path.join(self.filePath, self.fileName),
                                           # maxBytes=self.MAX_LOG_BYTES,
                                           # backupCount=self.BACK_UP_COUNT,
                                           delay=1
                                           )
        # 设定输出格式
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(message)s')
        # formatter.converter = time.localtime                                      # 时间转换
        self.handler.setFormatter(formatter)  # 格式加载到handler

    def create_logger(self):
        """建立Logger"""
        self.success_logger = logging.getLogger('Success')
        self.success_logger.propagate = False
        self.success_logger.addHandler(self.handler)

        self.failure_logger = logging.getLogger('Failure')
        self.failure_logger.propagate = False
        self.failure_logger.addHandler(self.handler)

        self.failure_logger = logging.getLogger('stderr')
        self.failure_logger.propagate = False
        self.failure_logger.addHandler(self.handler)

        self.requests_logger = logging.getLogger('requests')
        self.requests_logger.propagate = False
        self.requests_logger.addHandler(self.handler)

    def success_request(self, request_type, name, response_time, response_length):
        # 成功日志输出格式加载到Logger中
        msg = ' | '.join([str(request_type), name, str(response_time), str(response_length)])
        self.success_logger.info(msg)

    def failure_request(self, request_type, name, response_time, exception):
        msg = ' | '.join([str(request_type), name, str(response_time), str(exception)])
        self.failure_logger.info(msg)

    def execpt_error(self, locust_instance, exception, tb, *args, **kwargs):
        stderr_logger = logging.getLogger("stderr")
        stderr_logger.exception(exception)
        stderr_logger.exception('-' * 12)

    def get_locust_Hook(self):
        """钩子挂载到Locust中"""
        events.request_success += self.success_request
        events.request_failure += self.failure_request
        events.locust_error += self.execpt_error

    def get_locust_success_Hook(self):
        events.request_success += self.success_request

    def get_locust_failure_Hook(self):
        events.request_failure += self.failure_request

    def get_locust_error_Hook(self):
        events.locust_error += self.execpt_error

    def get_requests_log(self, method, path, requests, response):
        msg = ' | '.join([method, path, '请求数据: {}'.format(str(requests)), '返回数据: {}'.format(str(response))])
        self.requests_logger.info(msg)

