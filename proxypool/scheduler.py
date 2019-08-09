import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.settings import *

class Scheduler():
    def schedule_testter(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print("测试开始进行")
            tester.run()
            time.sleep(cycle)


    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print("代理池开始运行")
        if TESTER_ENABLED:
            test_process = Process(target=self.schedule_testter)
            test_process.start()

        if GETTER_ENABLED:
            get_process = Process(target=self.schedule_getter)
            get_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

