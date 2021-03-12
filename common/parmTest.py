# -*- coding: utf-8 -
import random
import string
from functools import reduce
from common.runMain import SendRequest


class AutoParmTest(SendRequest):

    # 生成参数验证的测试数据
    def generate_parm(self, mode, def_parm, parm_info):
        """
        :param mode: 生成数据的类型  0: 生成正确数据; 2:生成错误数据
        :param def_parm: 默认正确的参数 例如:{'a': 1, 'b': 2, 'c': 3}
        :param parm_info: 参数的字段信息 例如: [('a', {'require': True, 'value': ('1', '2'), 'length': 10}),
                                            ('b', {'require': True, 'number': (1, 8))]
            require: 必传
            value: 非必传，传入a视为正确值，传入(a, b)视为值域,与number必传其中一个
            number: 非必传,传入代表该参数是int或float类型，取值范围是1-8,与value必传其中一个
            length: 非必传，传入代表该参数是str类型，并且最大长度为10位，仅在参数是str类型时需要
        """
        parm_list = []
        for info in parm_info:
            # 获取name和require值
            name, require = info[0], info[1]['require']
            # 获取value、值length值、number值
            try: value = info[1]['value']
            except: value = None
            try: length = info[1]['length']
            except: length = None
            try: number = info[1]['number']
            except: number = None

            # 参数必须传入value、number其中一个
            if value is None and number is None:
                raise SystemExit("参数%s必须含有value、number其中一个信息" % name)
            if None not in [value, number]:
                raise SystemExit("参数%s只能含有value、number其中一个信息" % name)

            if number:
                if type(number) is not tuple or len(number) != 2:
                    raise SystemExit("参数%s的number信息必须是(0, 1)格式，请检查" % name)
                number_type = [type(num) for num in number]  # 获取number的字符类型列表
                if number_type not in [[float, float], [int, int], [int, float], [float, int]]:
                    raise SystemExit("参数%s的number信息必须是取值范围，请检查" % name)
                value = number  # number也是value的一种

            if length:
                if type(length) != int:
                    raise SystemExit("参数%s的length信息必须int字符，请检查" % name)

            # 处理value为单值情况
            if type(value) is not tuple: value = [value]
            # 获取value的字符类型列表
            value_type = set([type(val) for val in value])

            if mode == 0:
                for val in value:  # 传入值即为正确值
                    parm_list.append(dict(def_parm, **{name: val}))

                if number:  # 如果是数值区间，从区间随机生成一个数据
                    if int in value_type and len(value_type) == 1:  # 整数区间生成整数
                        parm_list.append(dict(def_parm, **{name: random.randint(value[0], value[1])}))
                    if float in value_type:  # 浮点数区间生成浮点数
                        parm_list.append(dict(def_parm, **{name: random.uniform(value[0], value[1])}))

                if length and str in value_type:  # 获取length值，只有str会有length
                    data = ''.join(random.sample(string.ascii_letters, length))
                    parm_list.append(dict(def_parm, **{name: data}))  # 有长度限制时，生成符合长度限制的随机字符串

                if require is False:  # 非必填参数的正确数据
                    parm_list.append(dict(def_parm, **{name: None}))  # 非必填参数的正确数据，要添加null传参
                    if str in value_type:
                        parm_list.append(dict(def_parm, **{name: ''}))  # 非必填str参数的正确数据，要添加空字符串''传参
                    elif dict in value_type:
                        parm_list.append(dict(def_parm, **{name: {}}))  # 非必填str参数的正确数据，要添加空字典{}传参
                    elif list in value_type:
                        parm_list.append(dict(def_parm, **{name: []}))  # 非必填str参数的正确数据，要添加空列表[]传参
                    # 非必填参数的正确数据，要不传该参数
                    new_parm = {}
                    for parm in def_parm:
                        if parm != name:
                            new_parm = dict(new_parm, **{parm: def_parm[parm]})
                    parm_list.append(new_parm)
            elif mode == 1:
                test_data = ["abc", 123, 4.56, [7, "def"], {'g': 8}, True]
                del_data = []
                for data in test_data:
                    if type(data) in value_type:
                        del_data.append(data)  # 记录需要删除的字符类型值，由于for循环和remove是按照坐标进行的
                for del_da in del_data:
                    test_data.remove(del_da)  # 参数的错误数据，首先需要移除正确的字符类型

                if number:
                    # 传入value为两个int时,并且是数值取值范围时
                    test_data.append(value[0]-1)
                    test_data.append(value[1]+1)

                if length and str in value_type:  # 获取length值，只有str会有length
                    data = ''.join(random.sample(string.ascii_letters, length+1))
                    test_data.append(data)  # 有长度限制时，生成超出长度限制的随机字符串

                if require is True:
                    test_data.append(None)  # 必填参数的错误数据，要添加null传参
                    if str in value_type:
                        test_data.append('')  # 必填str参数的错误数据，要添加空字符串''传参
                    elif dict in value_type:
                        test_data.append({})  # 必填dict参数的错误数据，要添加空字典{}传参
                    elif list in value_type:
                        test_data.append([])  # 必填list参数的错误数据，要添加空列表[]传参

                for data in test_data:
                    parm_list.append(dict(def_parm, **{name: data}))  # 返回处理之后的整个parm

                # 非必填参数的正确数据，要不传该参数
                if require is True:
                    new_parm = {}
                    for parm in def_parm:
                        if parm != name:
                            new_parm = dict(new_parm, **{parm: def_parm[parm]})
                    parm_list.append(new_parm)
        # 将生成的重复的parm删除
        func = lambda x, y: x if y in x else x + [y]
        parm_list = reduce(func, [[], ] + parm_list)
        return parm_list

    def autoParmTest(self, name, parm=None, del_parm=None, check=None, err_check=None):
        """
        :param name: 接口路径名称，如登录的phone接口写作：cgi/account/login/phone
        :param parm: api的请求参数中需要更新替换的k-v对
        :param del_parm: api的请求参数中需要删除的k-v对
        :param check: 验证参数正确的场景时需要该参数;不传不验证参数正确的场景
            check_code: 参数正确场景下的code检查点
            check_body: 参数正确场景下的body检查点
        :param err_check: 验证参数错误的场景时需要该参数;不传不验证参数错误的场景
            check_code: 参数错误场景下的code检查点
            check_body: 参数错误场景下的body检查点
        """
        def_parm = {}
        parm_info_list = []
        for par in parm:
            try:
                try:
                    value = parm[par]['value']
                except KeyError:
                    value = parm[par]['number']
                if type(value) is tuple:  # 如果参数值有多个
                    value = value[0]  # 取多个值的第一个为默认参数
                def_parm = dict(def_parm, **{par: value})  # 生成默认参数，例如{'a': 1, 'b': '2', 'c': '3'}
                parm_info_list.append((par, parm[par]))  # 生成需要的参数信息
            except:
                def_parm = dict(def_parm, **{par: parm[par]})

        # 如果有传check值，则进行参数正确场景下的验证
        if check:
            check_code, check_body = check['check_code'], check['check_body']  # 获取check_code，check_body
            test_parm_list = self.generate_parm(0, def_parm, parm_info_list)  # 获取测试需要的参数
            self.log.info('---验证点：必填、字符类型(正确)---')
            for test_parm in test_parm_list:
                del_parm_n = self.del_and_log(del_parm, test_parm, def_parm)  # 获取del_parm和打印对应的logo
                self.sendRequest(name=name, parm=test_parm, del_parm=del_parm_n,
                                 check_code=check_code, check_body=check_body)  # 调用基础请求，完成验证
        # 如果有传err_check值，则进行参数正确场景下的验证
        if err_check:
            check_code, check_body = err_check['check_code'], err_check['check_body']  # 获取check_code，check_body
            test_parm_list = self.generate_parm(1, def_parm, parm_info_list)  # 获取测试需要的参数
            self.log.info('---验证点：必填、字符类型(错误)---')
            for test_parm in test_parm_list:
                del_parm_n = self.del_and_log(del_parm, test_parm, def_parm)  # 获取del_parm和打印对应的logo
                self.sendRequest(name=name, parm=test_parm, del_parm=del_parm_n,
                                 check_code=check_code, check_body=check_body)  # 调用基础请求，完成验证

    # 处理不传字段和打印logo
    def del_and_log(self, del_parm, test_parm, def_parm):
        """
        :param del_parm: 外部传入的默认值
        :param test_parm: 变更后的参数字典
        :param def_parm: 默认的参数字典
        """
        if len(test_parm.keys()) != len(def_parm.keys()):
            name = [x for x in def_parm.keys() if x not in test_parm.keys()]
            self.log.info('---验证点：%s不传该参数---' % name[0])
            if del_parm is None: del_parm = []
            del_parm.append(name[0])
        else:
            for parm in test_parm:
                if test_parm[parm] != def_parm[parm]:
                    name, value = parm, test_parm[parm]
                    if value == '': value = '空字符串'
                    if value is None: value = 'null'
                    self.log.info('---验证点：%s传参数为%s---' % (name, value))
        return del_parm
        # 比较字典的方式，任意key的value为list时就无法进行比较
        # differ = set(test_parm.items()) ^ set(def_parm.items())
        # if len(differ) == 0:
        #     pass
        # elif len(differ) == 1:
        #     self.logInfo('---验证点：%s不传该参数---' % str(differ)[6:-3].split(','[0]))
        # else:
        #     name = str(differ)[5:-2].replace(' ', '').replace('(', '').replace(')', '').replace("'", '').split(',')[0]
        #     self.logInfo('---验证点：%s传参数为%s---' % (name, test_parm[name]))


if __name__ == "__main__":
    parm_info = [("body/parm1", {"value": (0, 86), "require": True}),
                 ("body/parm2", {"number": (1, 1.5), "require": True}),
                 ("body/parm3", {"value": 'abc', "require": True, 'length': 10}),
                 ("body/parm4", {"value": ('abc', 'def'), "require": True, 'length': 10}),
                 ("body/parm5", {"value": 'abc', "require": True}),
                 ("body/parm6", {"number": (10, 20), "require": True})]
    def_parm = {"body/parm1": 86, "body/parm2": 1, "body/parm3": 'abc', "body/parm4": 'abc', "body/parm5": 'abc', "body/parm6": 'abc'}
    print("正确")
    for parm in AutoParmTest().generate_parm(0, def_parm, parm_info):
        print(parm)
    print("错误")
    for parm in AutoParmTest().generate_parm(1, def_parm, parm_info):
        print(parm)
