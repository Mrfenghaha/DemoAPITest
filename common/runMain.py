# -*- coding: utf-8 -
import json
import requests
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common.logger import Log


class SendRequest:

    def send_get_request(self, method, url, headers, data):
        # 执行get请求
        result = requests.get(url=url, data=json.dumps(data), headers=headers).json()
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(method, url, headers, data, result).format()
        return result

    def send_post_request(self, method, url, headers, data):
        # 执行get请求
        result = requests.post(url=url, data=json.dumps(data), headers=headers).json()
        # 执行封装的打印方法，进行结果打印
        Print(method, url, headers, data, result).format()
        return result

    def send_post_file_request(self, method, url, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({'content-type': encode_data[1]}, **headers)
        new_data = encode_data[0]

        # 执行get请求
        result = requests.post(url=url, headers=new_headers, data=new_data).json()
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(method, url, headers, data, result).format()
        return result


class RunLocust(TaskSet):

    def run_get_locust(self, url, headers, data):
        # 执行get请求
        result = self.client.get(url=url, data=json.dumps(data), headers=headers).json()
        return result

    def run_post_locust(self, url, headers, data):
        # 执行get请求
        result = self.client.post(url=url, data=json.dumps(data), headers=headers).json()
        return result


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class RunMain(RunLocust, SendRequest):

    def sendRequest(self, parm):
        method = parm['method']
        url = parm['url']
        headers = parm['headers']
        data = parm['data']

        if method == "get" or "GET":
            return self.send_get_request(method, url, headers, data)
        elif method == "post" or "POST":
            return self.send_post_request(method, url, headers, data)
        elif method == "post_file" or "POST_FILE":
            return self.send_post_file_request(method, url, headers, data)
        else:
            print("method值错误或暂时不支持！！！")
            quit()

    def runLocust(self, parm):
        method = parm['method']
        url = parm['url']
        headers = parm['headers']
        data = parm['data']

        if method == "get" or "GET":
            return self.run_get_locust(url, headers, data)
        elif method == "post" or "POST":
            return self.send_post_locust(url, headers, data)
        else:
            print("method值错误或暂时不支持！！！")
            quit()


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
