# -*- coding: utf-8 -
import gevent.monkey
import json
import time
import requests
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common.readConfig import *
from common.logger import Log
from common.loggerLocust import LocustLogger
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class SendRequest:

    def send_post_file_request(self, url, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({"content-type": encode_data[1]}, **headers)
        new_data = encode_data[0]
        # 执行post请求
        result = requests.post(url=url, headers=new_headers, data=new_data)
        return result

    def sendRequest(self, parm):
        method = str.lower(parm['method'])  # 请求方式全部转化为小写
        url = host + parm['url']
        headers = parm['headers']
        data = parm['data']

        if method == "get":
            result = requests.get(url=url, data=json.dumps(data), headers=headers)
        elif method == "post":
            result = requests.post(url=url, data=json.dumps(data), headers=headers)
        elif method == "post_file":
            result = self.send_post_file_request(url, headers, data)
        else:
            print("method值错误或暂时不支持！！！")
            quit()
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(method, url, headers, data, result).format()
        return result


# 封装locust请求，将使用到的所有locust请求统一封装调用
class RunLocust(TaskSet):
    logger = LocustLogger(logs_locust_path, '%s.log' % time.strftime('%Y-%m-%d-%H'))
    logger.get_locust_Hook()

    def runLocust(self, parm):
        method = str.lower(parm['method'])  # 请求方式全部转化为小写
        url = parm['url']
        headers = parm['headers']
        data = parm['data']

        if method == "get":
            result = self.client.get(url=url, data=json.dumps(data), headers=headers)
        elif method == "post":
            result = self.client.post(url=url, data=json.dumps(data), headers=headers)
        else:
            print("method值错误或暂时不支持！！！")
            quit()
        return result


# 配置打印格式即美化、打印内容,同时完整的结果输出有利于报告的详细程度(就不再需要打log,报告内容是根据执行结果完成的)
class Print:
    # 构造函数，类接收外部传入参数全靠构造函数
    def __init__(self, method, url, headers, data, response):
        self.log = Log(logs_path, '%s.log' % time.strftime('%Y-%m-%d'))
        self.method = method
        self.url = url
        self.request_headers = headers
        self.request_body = data
        self.response = response
        self.response_code = response.status_code
        self.response_headers = response.headers

    # 对于部分内容进行格式转换(美化)
    def conversion(self):
        req_headers = json.dumps(self.request_headers, ensure_ascii=False, sort_keys=True, indent=2)
        req_body = json.dumps(self.request_body, ensure_ascii=False, sort_keys=True, indent=2)
        try:
            resp_headers = json.dumps(self.response_headers, ensure_ascii=False, sort_keys=True, indent=2)
            resp_body = json.dumps(self.response.json(), ensure_ascii=False, sort_keys=True, indent=2)
        except:
            resp_headers = ""
            resp_body = self.response.text
        return req_headers, req_body, resp_headers, resp_body

    def format(self):
        conversion = self.conversion()
        req_headers, req_body, resp_headers, resp_body = conversion[0], conversion[1], conversion[2], conversion[3]
        self.log.info(u"调用结果： \n%s" % "URL: " + self.url + "\nRequest Method: " + self.method
                      + "\nRequest Headers: \n" + req_headers + "\nRequest Body: \n" + req_body
                      + "\nResponse Status: " + str(self.response_code)
                      + "\nResponse Headers: \n" + resp_headers + "\nResponse Body: \n" + resp_body)
