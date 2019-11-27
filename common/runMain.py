# -*- coding: utf-8 -
import json
import requests
from common.logger import Log


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class RunMain:

    def __init__(self, method, url, headers, data):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data

    def send_get(self):
        # 执行get请求,并打印固定格式的执行内容、结果
        result = requests.get(url=self.url, data=json.dumps(self.data), headers=self.headers).json()

        # 执行封装的打印方法，进行结果打印
        Print('get', self.url, self.headers, self.data, result).format()

        return result

    def send_post(self):
        # 执行get请求,并打印固定格式的执行内容、结果
        result = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers).json()

        # 执行封装的打印方法，进行结果打印
        Print('post', self.url, self.headers, self.data, result).format()

        return result

    def send_post_file(self):
        # 执行get请求,并打印固定格式的执行内容、结果
        result = requests.post(url=self.url, headers=self.headers, data=self.data).json()

        # 执行封装的打印方法，进行结果打印
        Print('post_file', self.url, self.headers, self.data, result).format()

        return result

    def run_main(self):
        if self.method == 'get':
            result = self.send_get()
        elif self.method == 'post':
            result = self.send_post()
        elif self.method == 'post_file':
            result = self.send_post_file()
        else:
            print("method值错误！！！")
        return result


# 配置打印格式即美化、打印内容,同时完整的结果输出有利于报告的详细程度(就不再需要打log,报告内容是根据执行结果完成的)
class Print:
    # 构造函数，类接收外部传入参数全靠构造函数
    def __init__(self, method, url, headers, data, result):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.result = result
        self.log = Log()

    def format(self):
        # 对于部分内容进行格式转换并打印
        # json.dump()函数的使用，将json信息写进文件
        result = json.dumps(self.result, ensure_ascii=False, sort_keys=True, indent=2)
        headers = json.dumps(self.headers, ensure_ascii=False, sort_keys=True, indent=2)

        # 根据不同的请求方式打印不同的内容并打印log
        if self.method == 'get':
            # get请求不需要传data，所以结果也不需要打印data
            self.log.info(u'调用结果： \n%s' % 'API:' + self.url + '\nMethod:' + self.method + '\nHeaders: \n' + headers
                          + '\nResult: \n' + result)
        elif self.method == 'post':
            data = json.dumps(self.data, ensure_ascii=False, sort_keys=True, indent=2)
            # post请求打印所有传入的参数与结果
            self.log.info(u'调用结果： \n%s' % 'API:' + self.url + '\nMethod:' + self.method + '\nHeaders: \n' + headers
                          + '\nRequest Body: \n' + data + '\nResult: \n' + result)
        elif self.method == 'post_file':
            # post请求打印所有传入的参数与结果
            self.log.info(u'调用结果：\n%s' % 'API:' + self.url + '\nMethod:' + self.method + '\nHeaders: \n' + headers
                          + '\nResult: \n' + result)
        else:
            print("method值错误！！！")
