# 文档
* docs文件夹中有关于编写说明、项目结构、项目结构详细介绍的文档，请详细查看

# 环境准备
* 首先需要安装python3.x环境（linux系列不需要安装）
* 安装模块等

```
sudo pip3 install -r requirements.txt
```

# 编辑配置文件
* 编辑config/email.yaml文件,用于测试报告邮件发送
* 编辑config/env.yaml文件,用于数据库连接、host设置

# 用例执行说明
```
cd xxxx  # 进入根目录
python3 runcase.py $suite $name  # 执行用例
$suite 参数是文件夹路径
$name 参数是文件名称或all
例：
python3 runcase.py testcase/api_peso2go test_app_login  # 执行testcase/api_peso2go/test_app_login.py文件
python3 runcase.py testcase/api_peso2go all  # 执行testcase/api_peso2go文件夹下的所有py文件
```
