from locust import HttpLocust, TaskSet, task


# 定义用户行为
class UserBehavior(TaskSet):

    # 任一测试用例执行前均会执行一次
    def on_start(self):
        print('开始性能测试')

    @task(1)
    # 表示一个用户为行，访问百度首页。使用 @ task装饰该方法为一个事务。client.get()用于指请求的路径“ / ”，因为是百度首页，所以指定为根路径。
    def index(self):
        self.client.get("/")

    @task(2)  # task()参数用于指定该行为的执行权重。参数越大每次被虚拟用户执行的概率越高。如果不设置默认为1。
    def index2(self):
        self.client.get(
            "/s?wd=locust&rsv_spt=1&rsv_iqid=0xbb8514200006b7d0&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=8&rsv_sug1=9&rsv_sug7=101&rsv_sug2=0&inputT=1458&rsv_sug4=1911&rsv_sug=2")


# 用于设置性能测试
class WebsiteUser(HttpLocust):
    # 指向一个定义的用户行为类。
    task_set = UserBehavior

    # 执行事务之间用户等待时间的下界（单位：毫秒）。如果TaskSet类中有覆盖，以TaskSet 中的定义为准。
    min_wait = 3000

    # 执行事务之间用户等待时间的上界（单位：毫秒）。如果TaskSet类中有覆盖，以TaskSet中的定义为准。
    max_wait = 6000

    # 设置 Locust 多少秒后超时，如果为 None ,则不会超时。
    stop_timeout = 5

    # 一个Locust实例被挑选执行的权重，数值越大，执行频率越高。在一个 locustfile.py 文件中可以同时定义多个 HttpLocust 子类，然后分配他们的执行权重
    weight = 3

    # 脚本指定host执行测试时则不在需要指定
    host = "https://www.baidu.com"