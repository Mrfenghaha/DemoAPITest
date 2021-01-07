# -*- coding: utf-8 -
import gevent.monkey
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决，需要在引用requests前patch
import os
import ssl
import json
import time
import unittest
import requests
import websocket
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common import *
from common.log.logger import Log
# from common.log.loggerLocust import LocustLogger
# gevent.monkey.patch_all()


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class SendRequest():

    def websocket(self, url, Data):
        ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})  # 启动连接
        result_list = []
        for data in Data:
            ws.send(data)  # 发送请求
            result = ws.recv()  # 获取返回
            result_list.append(result)
            # 执行封装的打印方法，进行固定格式的结果打印
            Print().websocket(url, data, result)
        ws.close()  # 关闭连接
        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list

    def http(self, method, url, params, headers, body):
        # 发起请求
        if method == "POST_FILE":
            result = self.post_file(url, params, headers, body)
        elif method in ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE", "PATCH"]:
            result = requests.request(method=method, url=url, params=params, data=json.dumps(body), headers=headers)
        else:
            print("method值错误！！！")
            return False
        # 执行封装的打印方法，进行固定格式的结果打印
        Print().http(result)
        return {"code": result.status_code, "cookies": result.cookies.get_dict(), "headers": result.headers,
                "body": result.json(), "text": result.text, "content": result.content}

    def post_file(self, url, params, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({"content-type": encode_data[1]}, **headers)
        new_data = encode_data[0]
        # 执行post请求
        result = requests.post(url=url, params=params, headers=new_headers, data=new_data)
        # 执行封装的打印方法，进行固定格式的结果打印
        Print().http(headers)
        return result

    def get_api_json(self, api_name, parm):
        api_path = os.path.join(cur_path, "features/apis")
        json_file_list = []
        for root, dirs, files in os.walk(api_path):
            for f in files:
                fi = '%s/%s' % (root, f)  # 获取文件夹下的所有文件路径（包含子文件夹）
                if fi[-5:] == '.json':  # 找出.json结尾的文件
                    json_file_list = json_file_list + ['%s/%s' % (root, f)]

        num = 0
        for json_file in json_file_list:
            num += 1
            try:  # 根据api_name读取json内容
                file_info = open(json_file, encoding='utf-8')
                api_json = json.load(file_info)[api_name]  # 根据api名称获取json
                new_api_json = json.dumps(api_json)
                for key in parm.keys():  # 获取参数key
                    new_api_json = new_api_json.replace('"$%s"' % key, json.dumps(parm[key]))
                    new_api_json = new_api_json.replace('$%s' % key, json.dumps(parm[key]))
                file_info.close()
                return json.loads(new_api_json)
            except KeyError as error:
                if num == len(json_file_list):
                    print("错误: 接口%s不存在，请检查" % error)
                    return False  # 如果循环到最后一个还未找到则返回false

    # 根据检查点list验证
    def checkpoint(self, response, check_list):
        for checkpoint in check_list:
            for key in checkpoint.keys():
                resp = response
                for res in key.split('/'):
                    resp = resp[res]
                if checkpoint[key][0] == "assertEqual":
                    unittest.TestCase().assertEqual(resp, checkpoint[key][1], msg="%s与%s不相等")
                elif checkpoint[key][0] == "assertNotEqual":
                    unittest.TestCase().assertNotEqual(resp, checkpoint[key][1], msg="%s与%s相等")
                elif checkpoint[key][0] == "assertIn":
                    unittest.TestCase().assertIn(checkpoint[key][1], resp, msg="%s不包含%s" % (resp, checkpoint[key][1]))
                elif checkpoint[key][0] == "assertNotIn":
                    unittest.TestCase().assertNotIn(checkpoint[key][1], resp, msg="%s包含%s" % (resp, checkpoint[key][1]))

    def sendRequest(self, api_name, api_parm, *check):
        parm = self.get_api_json(api_name, api_parm)  # 根据api名称和替换参数，获取完成json
        try:
            protocol = str.upper(parm['protocol'])
            if protocol == "websocket":
                url = "wss://%s%s" % (host[parm['url'][0]].split("//")[1], parm['url'][1])
                data = parm['data']
                return self.websocket(url, data)
        except KeyError:
            # 请求方式需要统一转化为大写
            method, url, param, headers, data = str.upper(parm['method']), host + parm['url'], parm['params'], parm['headers'], parm['data']
            result = self.http(method, url, param, headers, data)
            if check != ():  # 如果传入检查点验证即进行验证，否则不做验证
                self.checkpoint(result, check[0])
            return result


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
    def __init__(self):
        self.log = Log(logs_path, '%s.log' % time.strftime('%Y-%m-%d'))

    def http(self, response):
        url = response.request.url
        method = response.request.method
        resp_code = response.status_code
        # 对于部分内容进行格式转换(美化)
        req_headers = json.dumps(dict(response.request.headers), ensure_ascii=False, sort_keys=True, indent=2).strip('"')
        req_body = json.dumps(response.request.body, ensure_ascii=False, sort_keys=True, indent=2).strip('"')
        resp_headers = json.dumps(dict(response.headers), ensure_ascii=False, sort_keys=True, indent=2).strip('"')
        try:
            resp_body = json.dumps(response.json(), ensure_ascii=False, sort_keys=True, indent=2).strip('"')
        except:
            resp_body = response.text
        # 打印接口请求结果
        self.log.info(u"调用结果： \nURL: %s\nRequest Method: %s\nRequest Headers:\n%s\nRequest Body:\n%s"
                      u"\nResponse Status:%s\nResponse Headers:\n%s\nResponse Body:\n%s"
                      % (url, method, req_headers, req_body, resp_code, resp_headers, resp_body))

    def websocket(self, url, body, response):
        # 打印接口请求结果
        self.log.info(u"调用结果： \nURL: %s\nRequest Body:\n%s\nResponse Body:\n%s"
                      % (url, body, response))
