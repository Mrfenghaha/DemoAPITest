# -*- coding: utf-8 -
import gevent.monkey
gevent.monkey.patch_all()  # python3.6及以上会因为gevent产生无限递归问题，需要添加此方法解决，需要在引用requests前patch
import os
import ssl
import json
import yaml
import time
import unittest
import requests
import unittest
import websocket
from urllib3 import encode_multipart_formdata
from locust import TaskSet
from common import *
from common.log.logger import Log
from features.function import CustomFunc
from features.data import custom_data
# from common.log.loggerLocust import LocustLogger
# gevent.monkey.patch_all()


# 配置打印格式即美化、打印内容,同时完整的结果输出有利于报告的详细程度(就不再需要打log,报告内容是根据执行结果完成的)
class Print:
    # 构造函数，类接收外部传入参数全靠构造函数
    def __init__(self):
        self.log = Log(logs_path, '%s.log' % time.strftime('%Y-%m-%d'))

    def http_log(self, response):
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

    def websocket_log(self, url, body, response):
        # 打印接口请求结果
        self.log.info(u"调用结果： \nURL: %s\nRequest Body:\n%s\nResponse Body:\n%s"
                      % (url, body, response))


# 封装requests请求，将使用到的所有requests请求统一封装调用,并打印美化格式的结果
class SendRequest(Print, unittest.TestCase):
    env = env  # 声明环境变量
    data = custom_data  # 声明自定义生成数据
    func = CustomFunc()  # 声明自定义函数
    path = cur_path  # 声明根路径

    # 发起请求的对外方法函数
    def sendRequest(self, name, parm=None, del_parm=None, check_code=None, check_headers=None, check_body=None,
                    mode='http'):
        api_json = self.get_api_json(name, parm, del_parm)  # 根据api名称和替换参数，获取完整json
        if mode == "http":
            method, url, params, headers, body = api_json['method'], api_json['url'], api_json['params'], \
                                                 api_json['headers'], api_json['body']
            url = env['host'] + env['prefix'] + url
            check = {"chk_code": check_code, "chk_headers": check_headers, "chk_body": check_body}
            return self.http(method, url, params, headers, body, check)
        elif mode == "uploadFile":
            method, url, params, headers, body = api_json['method'], api_json['url'], api_json['params'], \
                                                 api_json['headers'], api_json['body']
            url = env['host'] + env['prefix'] + url
            # 做文件加密
            encode_data = encode_multipart_formdata(body)
            headers = dict(headers, **{"content-type": encode_data[1]})
            body = encode_data[0]

            check = {"chk_code": check_code, "chk_headers": check_headers, "chk_body": check_body}
            return self.http(method, url, params, headers, body, check)
        elif mode == "websocket":
            url = "wss://%s%s" % (env["host"][api_json['url'][0]].split("//")[1], api_json['url'][1])
            data = api_json['data']
            return self.websocket(url, data)

    def check_status_code(self, status_code, expect_code):
        """检查`status_code`是否等于`expect_code`"""
        if expect_code:
            if int(expect_code):
                self.assertEqual(status_code, int(expect_code), msg="检查点错误，status_code实际为%s，不等于%s" % (status_code, str(expect_code)))
            else:
                raise ValueError("错误: 检查点code期望值%s有误" % expect_code)

    def check_json(self, json_data, checkpoint):
        """检查`json指定值`是否等于`checkpoint`"""
        if checkpoint:
            for key in checkpoint.keys():
                data = json_data
                for d in key.split('/'):
                    try:  # 尝试将路径中的数字转为int类型，否则正常使用路径
                        data = data[int(d)]
                    except ValueError:
                        data = data[d]
                op, exp_val = checkpoint[key]
                if op == "=":
                    self.assertEqual(data, exp_val, msg="检查点错误，%s值为%s，不等于%s" % (key, data, exp_val))
                elif op == "!=":
                    self.assertNotEqual(data, exp_val, msg="检查点错误，%s值为%s，等于%s" % (key, data, exp_val))
                elif op == ">":
                    self.assertGreater(data, exp_val, msg="检查点错误，%s值为%s，不大于%s" % (key, data, exp_val))
                elif op == "<":
                    self.assertLess(data, exp_val, msg="检查点错误，%s值为%s，不小于%s" % (key, data, exp_val))
                elif op == ">=":
                    self.assertGreaterEqual(data, exp_val, msg="检查点错误，%s值为%s，不大于等于%s" % (key, data, exp_val))
                elif op == "<=":
                    self.assertLessEqual(data, exp_val, msg="检查点错误，%s值为%s，不小于等于%s" % (key, data, exp_val))
                elif op == "in":
                    self.assertIn(exp_val, data, msg="检查点错误，%s值为%s，不包含%s" % (key, data, exp_val))
                elif op == "not-in":
                    self.assertNotIn(exp_val, data, msg="检查点错误，%s值为%s，包含%s" % (key, data, exp_val))
                elif op == "type":
                    self.assertTrue(exp_val is type(data), msg="检查点错误，%s值为%s，类型不为%s" % (key, data, exp_val))
                else:
                    self.assertTrue(False, msg="检查点对比方式错误，或当前不支持该方式")

    def read_api_json(self, path):
        """获取api的json obj"""
        file_path, file_name = path.rsplit("/", 1)
        api_path = os.path.join(cur_path, "features", "apis", file_path)
        files = os.listdir(api_path)
        api_path = api_path+"/"+file_name

        if file_name+".yaml" in files:
            with open(api_path+".yaml", 'r') as f:
                api_json = yaml.full_load(f)  # 根据api名称获取json
        elif file_name+".json" in files:
            with open(api_path+".json", 'r') as f:
                api_json = json.load(f)  # 根据api名称获取json
        else:
            raise ValueError("错误: 接口%s不存在，请检查路径是否正确" % path)

        if api_json['params'] is None: api_json['params'] = {}
        if api_json['headers'] is None: api_json['headers'] = {}
        if not api_json.get('body'): api_json['body'] = {}
        return api_json

    def update_api_json(self, api_json, parm):
        """替换api中的参数"""
        if parm:
            for key in parm.keys():  # 获取参数key
                paths = key.split('/')  # 根据传入key获取路径
                if len(paths) == 1: # 防止有同学参数化名称为url、body、params、method、headers，json文件中整块被误替换，顾只有xx/xx格式名称被视为字典路径替换
                    api_json = json.dumps(api_json)  # 将json转为str，用于字符替换
                    api_json = api_json.replace('"$%s"' % key, json.dumps(parm[key]))\
                        .replace('$%s' % key, json.dumps(parm[key]).strip('"'))  # 找到$%s进行替换
                    api_json = json.loads(api_json)  # json转为字典
                else:
                    dict_path = []
                    for path in paths:  # 将路径中的数字转为int类型
                        try:
                            dict_path.append(int(path))
                        except ValueError:
                            dict_path.append(path)
                    # 下述方法为替换json中指定的key对应的value值（方法比较笨，如果有更好的方法可以替换）
                    if len(dict_path) == 2:
                        api_json[dict_path[0]][dict_path[1]] = parm[key]
                    elif len(dict_path) == 3:
                        api_json[dict_path[0]][dict_path[1]][dict_path[2]] = parm[key]
                    elif len(dict_path) == 4:
                        api_json[dict_path[0]][dict_path[1]][dict_path[2]][dict_path[3]] = parm[key]
                    elif len(dict_path) == 5:
                        api_json[dict_path[0]][dict_path[1]][dict_path[2]][dict_path[3]][dict_path[4]] = parm[key]
        return api_json

    def del_api_json(self, api_json, del_parm):
        if del_parm:
            dict_path = []
            for parm in del_parm:  # 获取参数key
                paths = parm.split('/')  # 根据传入key获取路径
                for path in paths:  # 将路径中的数字转为int类型
                    try:
                        dict_path.append(int(path))
                    except ValueError:
                        dict_path.append(path)
                # 下述方法为替换json中指定的key对应的value值（方法比较笨，如果有更好的方法可以替换）
                if len(dict_path) == 2:
                    del api_json[dict_path[0]][dict_path[1]]
                elif len(dict_path) == 3:
                    del api_json[dict_path[0]][dict_path[1]][dict_path[2]]
                elif len(dict_path) == 4:
                    del api_json[dict_path[0]][dict_path[1]][dict_path[2]][dict_path[3]]
                elif len(dict_path) == 5:
                    del api_json[dict_path[0]][dict_path[1]][dict_path[2]][dict_path[3]][dict_path[4]]
        return api_json

    def get_api_json(self, path, parm, del_parm):
        api_json = self.read_api_json(path)  # 获取api的json内容
        api_json = self.update_api_json(api_json, parm)  # 更新json内容
        api_json = self.del_api_json(api_json, del_parm)  # 删除json内容
        api_json['method'] = api_json['method'].upper()  # 修改json中的method为统一大写
        return api_json

    def http(self, method, url, params, headers, body, check):
        """发起http请求,并验证检查点

        :param method:
        :param url:
        :param params:
        :param headers:
        :param body:
        :param check: obj, 支持的key：chk_code, chk_headers, chk_body
        """
        if method in ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE", "PATCH"]:
            result = requests.request(method=method, url=url, headers=headers, params=params, data=json.dumps(body))
        else:
            raise SystemExit("错误: %s method值不支持" % method)
        self.http_log(result)
        # 检查点验证
        if check:
            status_code, headers, body = result.status_code, result.headers, result.json()
            chk_code, chk_headers, chk_body = check.get("chk_code"), check.get("chk_headers"), check.get("chk_body")
            self.check_status_code(status_code, chk_code)
            self.check_json(headers, chk_headers)
            self.check_json(body, chk_body)
        return result

    def post_file(self, url, params, headers, data):
        # 文件转化为二进制流
        encode_data = encode_multipart_formdata(data)
        new_headers = dict({"content-type": encode_data[1]}, **headers)
        new_data = encode_data[0]
        # 执行post请求
        result = requests.post(url=url, params=params, headers=new_headers, data=new_data)
        # 执行封装的打印方法，进行固定格式的结果打印
        self.http_log(headers)
        return result

    def websocket(self, url, Data):
        ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})  # 启动连接
        result_list = []
        for data in Data:
            ws.send(data)  # 发送请求
            result = ws.recv()  # 获取返回
            result_list.append(result)
            # 执行封装的打印方法，进行固定格式的结果打印
            self.websocket_log(url, data, result)
        ws.close()  # 关闭连接
        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list


# 封装locust请求，将使用到的所有locust请求统一封装调用
class RunLocust(TaskSet, SendRequest):
    # logger = LocustLogger(logs_locust_path, '%s.log' % time.strftime('%Y-%m-%d-%H'))
    # logger.get_locust_Hook()

    def runLocust(self, name, parm=None, del_parm=None):
        api_json = self.get_api_json(name, parm, del_parm)  # 根据api名称和替换参数，获取完整json
        method, url, params, headers, body = str.lower(api_json['method']), api_json['url'], api_json['params'], \
                                             api_json['headers'], api_json['body']
        url = env['host'] + env['prefix'] + url

        if method == "get":
            result = self.client.get(url=url, data=json.dumps(body), headers=headers)
        elif method == "post":
            result = self.client.post(url=url, data=json.dumps(body), headers=headers)
        elif method == "put":
            result = self.client.put(url=url, data=json.dumps(body), headers=headers)
        elif method == "delete":
            result = self.client.delete(url=url, data=json.dumps(body), headers=headers)
        elif method == "options":
            result = self.client.options(url=url, data=json.dumps(body), headers=headers)
        elif method == "head":
            result = self.client.head(url=url, data=json.dumps(body), headers=headers)
        elif method == "patch":
            result = self.client.patch(url=url, data=json.dumps(body), headers=headers)
        else:
            raise SystemExit("method值错误！！！")
        return result
