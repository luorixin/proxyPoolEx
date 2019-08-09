import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.settings import *

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = "http://"+proxy
                print("正常测试代理", proxy)
                async with session.get(TEST_URL, proxy = real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS:
                        self.redis.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.derease(proxy)
                        print("请求验证不合法", response.status, 'IP', proxy)
            except(ClientError, aiohttp.ClientProxyConnectionError, asyncio.TimeoutError, AttributeError):
                self.redis.derease(proxy)
                print("请求代理失败", proxy)

    def run(self):
        print("测试开始")
        try:
            count = self.redis.count()
            print("当前剩余：",count, "个代理")
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                print("正在测试第",start+1, '-', stop, "个代理")
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print("测试发送错误", e.args)





