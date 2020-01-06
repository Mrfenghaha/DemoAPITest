# -*- coding: utf-8 -
from locust import HttpLocust, TaskSet, task
from random import randint


user_type = "ordinary"


# Web性能测试
class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    # 随机返回登录用户
    def login_user(self):
        users = {"user1": 123456, "user2": 123123, "user3": 111222}
        data = randint(1, 3)
        username = "user"+str(data)
        password = users[username]
        return username, password

    @task
    def login(self):
        username, password = self.login_user()[0], self.login_user()[1]
        self.client.post("/login_action", {"username": username, "password": password, "user_type": user_type})


class User(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
    host = 'https://debugtalk.com'
