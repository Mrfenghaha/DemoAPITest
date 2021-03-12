# 框架介绍
该框架为Http、Https、WebSocket接口测试框架，可进行接口功能测试、接口工作流等测试，同时也支持Http、Https性能测试。

由于考虑每个不同项目接口规范、接口定义方式均有不同，为保持灵活性，本框架对于用例编写部分并未进行更多的封装，使用本框架仍需要一些Python编码基础


# 框架详细介绍

![](https://github.com/fengyibo963/DemoAPITest/blob/master/docs/%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84.jpg)

## 用例分层概念介绍
该框架分层使用BDD理念（参考HttpRunner的分层理念）

* API（接口）：封装接口测试调用的接口
* Suite（套件）：封装动作(行为)（动作：例如登录动作可能调用发送验证码、登录两个接口，但由于仅支持验证码登录，即可将这两个接口一起封装为登录的动作）
* TestCase（用例）：使用动作(行为)拼接工作流，并且对于所有动作可以进行断言

由于某些接口自身就可以定义为动作，因为TestCase既可以使用动作拼接，也可以使用API进行拼接（或混合拼接）。

如果为了更好的理解分层，同时增强TestCase脚本的可读性，可以封装所有动作仅使用Suite拼接TestCase（单同时代码量、维护成本会相应的增高）

TestCase拼接为简单关键字驱动模式，使用动作的函数名或类型作为关键字，并且Python语言自身按照顺序执行的机制，达到直接拼接的效果

## 简单数据驱动介绍
对于API层所有的接口均进行高度参数化，将请求需要的所有参数进行参数化，这样使得API复用性、维护性提高

所有对于接口的测试场景，仅直接通过不同的测试数据组合实现

## 数据库操作介绍
由于一些原因可能需要断言的数据并不能从Response中获取仅仅记录在数据库，或者需要清理自动化测试产生的系统数据等，造成需要添加数据库操作拓展

## 数据生成器介绍
接口需要的参数有一些并不能固定设置，例如时间戳、UUID等不可重复参数，或者因为业务需要不能重复的手机号等等参数。

为了做到真正的自动化扩展使用数据生成器，使用生成器按照规则生成想要的数据字典，在编写TestCase的使用直接调用生成器并提取参数即可

## 性能测试介绍
Locust是一个很好用并且使用协程而非进程/线程的工具，大大增加了单机并发量。相关学习可[参考](https://blog.csdn.net/baidu_36943075/article/details/102605126)

由于Locust工具的使用简单，只需要测试用例的基础上增加相应的并发设置即可，因此Locust可以直接引用TestCase拼接好的用例

## 项目结构详细介绍

```
|-- common      # 基础通用方法，使用过程中基本无需修改（可以二次开发自行拓展）
|    -- log      # log打印
|        -- logger.py  # 功能测试log输出配置
|        -- loggerLocust.py  # Locust性能测试log输出配置
|    -- run      # 运行用例的方法
|        -- emailSend.py  # 测试执行后的邮件发送配置(收件人配置)
|        -- envSpecify.py  # env环境切换方法
|        -- htmlTestRunner.py  # unittest测试执行生成测试报告的报告文件
|        -- runCase.py     # 通过参数执行任一测试用例或测试用例集
|    -- __init__.py  # 所有需要自动创建的文件和默认文件、读取环境变量 
|    -- runMain.py  # 接口请求整体封装
|-- config
|    -- email.yaml  # 邮件发送邮箱配置
|    -- env.yaml  # 环境变量
|    -- envDev.yaml  # 开发环境配置文件，可以根据自己需要添加删除
|    -- envSt.yaml  # 测试环境配置文件，可以根据自己需要添加删除
|-- databases
|    -- xxxx.py  # 某些数据库操作的封装
|    -- pubilc.py  # 数据库链接的基础
|-- docs
|-- result
|    -- logs   # 生成的log文件存储位置
|    -- logsLocust   # 生成的Locust的log文件存储位置
|    -- reports     # 生成的测试报告存储位置
|-- features
|    -- api
|        -- xxxx.yaml  # 该产品某一接口(一个接口一个文件)
|    -- suites
|        -- xxxx.py  # 该产品通用封装的模块
|    -- testcases
|        -- func  # 某产品线功能逻辑测试用例
|        -- interface  # 某产品api测试用例
|        -- smoke # 某产品冒烟测试用例
|            -- xxx_test.py  # 测试用例文件
|    -- locust
|        -- xxxx_test.py  # 性能测试脚本文件
|    -- data.py  # 通用方数据生成文件
|    -- function.py  # 通用方法的文件
|-- main.py    # 自动化框架执行入口
|-- requirements.txt    # 该文件记录所有需要用的框架（以便更换环境一键安装）
```

# 环境/使用介绍
## 环境说明
python3环境
安装相关模块库
```
pip3 install -r requirements.txt
```
## 配置说明
1. 邮件发送
    * config/email.yaml文件,用于测试报告邮件发送，需要配置邮箱相关信息
2. 配置env环境参数
    * config/env.yaml文件,用于数据库连接、host设置
    * envDev.yaml/envSt.yaml分别为对应环境的配置信息
    * 可以添加更多环境，直接添加相应的envXx.yaml文件即可，运行用例时使用Xx作为环境参数即可 
    * 当需要多环境执行时，env.yaml文件变为数据传输中介不再需要维护

## 功能用例执行说明
runcase.py脚本为功能测试用例执行统一入口

**查看帮助--help**
```
python3 main.py --help
usage: main.py [-h] [--env ENV] [--collection COLLECTION] --name NAME

optional arguments:
  -h, --help            show this help message and exit
  --env ENV, -e ENV     环境变量参数，非必要参数
  --collection COLLECTION, -c COLLECTION
                        测试用例集合名称，非必要参数(testcases中用于划分用例集合的文件夹名,当未划分用例集合时不需要)
  --name NAME, -n NAME  测试用例名称，必要参数
```

**执行用例**

```
python3 main.py -e $env -c $collection -n $name  # 在$env环境下,执行用例,$collection文件夹路径,$name文件名称或all(all即可该用例集下左右用例)
例：
python3 main.py -c api_test -n test_login
python3 main.py -c api_test -n all
python3 main.py -e St -c api_test -n all
```

**执行性能测试**
* web执行
```
locust -f features/testcase/locust/mostAPI_test.py
```
通过浏览器访问：http://localhost:8089  设置模拟用户数、每秒产生（启动）的虚拟用户数即可开始测试，可通过Ctrl+C关闭服务
* no-web执行
```
locust -f tests/testcase/locust/test_mostAPI.py --no-web -c 2 -r 1 -t 3
```
-c 设置虚拟用户数。
-r 设置每秒启动虚拟用户数。
-t 设置设置运行时间。

