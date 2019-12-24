# 文档
* docs文件夹中有关于编写说明、项目结构、项目结构详细介绍的文档，请详细查看

# 环境准备
* 首先需要安装python3.x环境（linux系列不需要安装）
* 安装模块库
```
pip3 install -r requirements.txt
```

## 编辑配置文件
### 配置邮件发送
* 编辑config/email.yaml文件,用于测试报告邮件发送
### 配置env环境参数
* 编辑config/envDev.yaml文件,用于开发环境数据库连接、host设置
* 编辑config/envSt.yaml文件,用于测试环境数据库连接、host设置
* 可以添加更多环境，直接添加相应的envXx.yaml文件即可，运行用例是使用Xx作为参数即可 
* 无需维护env.yaml文件，它仅做传输中介

# 用例执行说明
```
python3 runcase.py $env $suite $name  # 在$env环境下,执行用例,$suite文件夹路径,$name文件名称或all
例：
python3 runcase.py Dev testcase/api_test test_login  # 在开发环境下，执行testcase/api_test/test_login用例
python3 runcase.py St testcase/api_test all  # 在测试环境下，执行testcase/api_test文件夹下的所有用例
```
