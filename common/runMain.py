# -*- coding: utf-8 -
import gevent.monkey
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决，需要在引用requests前patch
import ssl
import json
import time
import requests
import websocket
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common import *
from common.log.logger import Log
# from common.log.loggerLocust import LocustLogger
# gevent.monkey.patch_all()


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class SendRequest:

    def websocket(self, url, Data):
        ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})  # 启动连接
        result_list = []
        for data in Data:
            ws.send(data)  # 发送请求
            result = ws.recv()  # 获取返回
            result_list.append(result)
            # 执行封装的打印方法，进行固定格式的结果打印
            Print(url, data, result).websocket()
        ws.close()  # 关闭连接
        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list

    def http(self, method, url, headers, data):
        if method == "get":
            result = requests.get(url=url, data=json.dumps(data), headers=headers)
        elif method == "post":
            result = requests.post(url=url, data=json.dumps(data), headers=headers)
        elif method == "post_file":
            result = self.send_post_file_request(url, headers, data)
        elif method == "put":
            result = requests.put(url=url, data=json.dumps(data), headers=headers)
        elif method == "delete":
            result = requests.delete(url=url, data=json.dumps(data), headers=headers)
        elif method == "options":
            result = requests.options(url=url, data=json.dumps(data), headers=headers)
        elif method == "head":
            result = requests.head(url=url, data=json.dumps(data), headers=headers)
        elif method == "patch":
            result = requests.patch(url=url, data=json.dumps(data), headers=headers)
        else:
            print("method值错误！！！")
            quit()
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(url, data, result).http(method, headers)
        return result

    def send_post_file_request(self, url, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({"content-type": encode_data[1]}, **headers)
        new_data = encode_data[0]
        # 执行post请求
        result = requests.post(url=url, headers=new_headers, data=new_data)
        # 执行封装的打印方法，进行固定格式的结果打印
        Print(url, data, result).http("post", headers)
        return result

    def sendRequest(self, parm):
        try:
            protocol = str.lower(parm['protocol'])
            if protocol == "websocket":
                url = "wss://%s%s" % (host[parm['url'][0]].split("//")[1], parm['url'][1])
                data = parm['data']
                return self.websocket(url, data)
        except:
            method = str.lower(parm['method'])  # 请求方式全部转化为小写
            url = host + parm['url']
            headers = parm['headers']
            data = parm['data']
            return self.http(method, url, headers, data)


# 封装locust请求，将使用到的所有locust请求统一封装调用
class RunLocust(TaskSet):
    # logger = LocustLogger(logs_locust_path, '%s.log' % time.strftime('%Y-%m-%d-%H'))
    # logger.get_locust_Hook()

    def runLocust(self, parm):
        method = str.lower(parm['method'])  # 请求方式全部转化为小写
        url = parm['url']
        headers = parm['headers']
        data = parm['data']

        if method == "get":
            result = self.client.get(url=url, data=json.dumps(data), headers=headers)
        elif method == "post":
            result = self.client.post(url=url, data=json.dumps(data), headers=headers)
        elif method == "post_file":
            encode_data = encode_multipart_formdata(data)  # 文件转化为二进制流
            new_headers = dict({"content-type": encode_data[1]}, **headers)
            new_data = encode_data[0]
            result = self.client.post(url=url, headers=new_headers, data=new_data)
        elif method == "put":
            result = self.client.put(url=url, data=json.dumps(data), headers=headers)
        elif method == "delete":
            result = self.client.delete(url=url, data=json.dumps(data), headers=headers)
        elif method == "options":
            result = self.client.options(url=url, data=json.dumps(data), headers=headers)
        elif method == "head":
            result = self.client.head(url=url, data=json.dumps(data), headers=headers)
        elif method == "patch":
            result = self.client.patch(url=url, data=json.dumps(data), headers=headers)
        else:
            print("method值错误！！！")
            quit()
        return result


# 配置打印格式即美化、打印内容,同时完整的结果输出有利于报告的详细程度(就不再需要打log,报告内容是根据执行结果完成的)
class Print:
    # 构造函数，类接收外部传入参数全靠构造函数
    def __init__(self, url, data, response):
        self.log = Log(logs_path, '%s.log' % time.strftime('%Y-%m-%d'))
        self.url = url
        self.request_body = data
        self.response = response

    def http(self, method, headers):
        method = method
        request_headers = headers
        response_code = str(self.response.status_code)
        response_headers = self.response.headers
        # 对于部分内容进行格式转换(美化)
        req_headers = json.dumps(request_headers, ensure_ascii=False, sort_keys=True, indent=2)
        req_body = json.dumps(self.request_body, ensure_ascii=False, sort_keys=True, indent=2)
        try:
            resp_headers = json.dumps(response_headers, ensure_ascii=False, sort_keys=True, indent=2)
            resp_body = json.dumps(self.response.json(), ensure_ascii=False, sort_keys=True, indent=2)
        except:
            resp_headers = ""
            resp_body = self.response.text
        # 打印接口请求结果
        self.log.info(u"调用结果： \nURL: %s\nRequest Method: %s\nRequest Headers:\n%s\nRequest Body:\n%s"
                      u"\nResponse Status:%s\nResponse Headers:\n%s\nResponse Body:\n%s"
                      % (self.url, method, req_headers, req_body, response_code, resp_headers, resp_body))

    def websocket(self):
        # 打印接口请求结果
        self.log.info(u"调用结果： \nURL: %s\nRequest Body:\n%s\nResponse Body:\n%s"
                      % (self.url, self.request_body, self.response))
