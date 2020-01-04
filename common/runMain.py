# -*- coding: utf-8 -
import gevent.monkey
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决
import json
import requests
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common.logger import Log
from common.readConfig import *


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class SendRequest:

    def send_get_request(self, method, url, headers, data):
        # 执行get请求
        result = requests.get(url=url, data=json.dumps(data), headers=headers)
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(method, url, headers, data, result).format()
        return result

    def send_post_request(self, method, url, headers, data):
        # 执行get请求
        result = requests.post(url=url, data=json.dumps(data), headers=headers)
        # 执行封装的打印方法，进行结果打印
        Print(method, url, headers, data, result).format()
        return result

    def send_post_file_request(self, method, url, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({"content-type": encode_data[1]}, **headers)
        new_data = encode_data[0]

        # 执行get请求
        result = requests.post(url=url, headers=new_headers, data=new_data)
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(method, url, headers, data, result).format()
        return result

    def sendRequest(self, parm):
        method = parm['method']
        url = host + parm['url']
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


# 封装locust请求，将使用到的所有locust请求统一封装调用
class RunLocust(TaskSet):

    def run_get_locust(self, url, headers, data):
        # 执行get请求
        result = self.client.get(url=url, data=json.dumps(data), headers=headers)
        return result

    def run_post_locust(self, url, headers, data):
        # 执行get请求
        result = self.client.post(url=url, data=json.dumps(data), headers=headers)
        return result

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
    def __init__(self, method, url, headers, data, response):
        self.log = Log()
        self.method = method
        self.url = url
        self.request_headers = headers
        self.request_body = data
        self.response = response
        self.response_code = response.status_code
        self.response_headers = response.headers
        self.response_body = response.status_code

    # 对于部分内容进行格式转换(美化)
    def conversion(self):
        request_headers = json.dumps(self.request_headers, ensure_ascii=False, sort_keys=True, indent=2)
        request_body = json.dumps(self.request_body, ensure_ascii=False, sort_keys=True, indent=2)
        try:
            response_headers = json.dumps(self.response_headers, ensure_ascii=False, sort_keys=True, indent=2)
            response_body = json.dumps(self.response.json(), ensure_ascii=False, sort_keys=True, indent=2)
        except:
            response_headers = ""
            response_body = self.response.text
        return request_headers, request_body, response_headers, response_body

    def format(self):
        conversion = self.conversion()
        request_headers = conversion[0]
        request_body = conversion[1]
        response_headers = conversion[2]
        response_body = conversion[3]
        self.log.info(u"调用结果： \n%s" % "URL:" + self.url + "\nRequest Method:" + self.method
                      + "\nRequest Headers: \n" + request_headers + "\nRequest Body: \n" + request_body
                      + "\nResponse Headers: \n" + response_headers + "\nResponse Body: \n" + response_body)
