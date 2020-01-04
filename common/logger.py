# -*- coding: utf-8 -
import os
import time
import logging


# log_path是存放日志的路径
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
res_path = os.path.join(cur_path, "result")
log_path = os.path.join(res_path, 'logs')
# 如果不存在这个result/logs文件夹，就自动创建一个
if not os.path.exists(res_path):
    os.mkdir(res_path)
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log():
    def __init__(self):
        # 文件的命名
        self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y-%m-%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        # self.formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: \n%(message)s')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s: \n%(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == "__main__":
    log = Log()
    log.info("---测试开始----")
    log.info("操作步骤1,2,3")
    log.warning("----测试结束----")
