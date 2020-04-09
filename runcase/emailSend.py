# -*- coding: utf-8 -
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from common.readConfig import *


class EmailSend:
    def get_new_report(self):
        # ======查找测试目录，找到最新生成的测试报告文件======
        cur_path = os.path.dirname(os.path.realpath(__file__))
        test_report = os.path.join(os.path.dirname(cur_path), 'reports')
        lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
        lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))  # 按时间排序
        print(('最新的文件是：' + lists[-1]))
        file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
        return file_new

    def email_send(self):
        file_new = self.get_new_report()

        # ==============定义发送邮件==========
        # 读取报告文件，获取报告信息
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()

        email_sender = email_info['email_sender']
        email_receiver = email_info['email_receiver']
        email_server = email_info['email_server']
        email_password = email_info['email_password']

        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['From'] = email_sender
        msg['To'] = ','.join(email_receiver)   # 多人时,receiver使用数组,并转换;单人时直接书写即可
        msg['Subject'] = Header("接口自动化测试报告", 'utf-8')

        smtp = smtplib.SMTP()
        smtp.connect(email_server)  # 邮箱服务器
        smtp.login(email_sender, email_password)  # 登录邮箱
        smtp.sendmail(email_sender, email_receiver, msg.as_string())  # 发送者和接收者
        smtp.quit()
        print("邮件已发出！注意查收。")


if __name__ == "__main__":
    EmailSend().email_send()
