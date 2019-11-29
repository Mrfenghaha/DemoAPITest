# 文档
* docs文件夹中有关于编写说明、项目结构、项目结构详细介绍的文档，请详细查看

# 环境准备
* 首先需要安装python3.x环境（linux系列不需要安装）
* 安装模块库
```
pip3 install -r requirements.txt
```

# 编辑配置文件
* 编辑config/email.yaml文件,用于测试报告邮件发送
* 编辑config/env.yaml文件,用于数据库连接、host设置

# 用例执行说明
```
python3 runcase.py $suite $name  # 执行用例,$suite文件夹路径,$name文件名称或all
例：
python3 runcase.py testcase/api_test test_login  # 执行testcase/api_test/test_login用例
python3 runcase.py testcase/api_test all  # 执行testcase/api_test文件夹下的所有用例
```
