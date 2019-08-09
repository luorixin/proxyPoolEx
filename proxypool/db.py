import redis
from proxypool.error import PoolEmptyError
from proxypool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re

class RedisClient(object):
  def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
    self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
  
  def add(self, proxy, score=INITIAL_SCORE):
    if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
      print('代理不符合规范', proxy, '丢弃')
      return
    if not self.db.zscore(REDIS_KEY, proxy):
      return self.db.zadd(REDIS_KEY, {proxy: score})

  def random(self):
    """
    随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
    :return: 随机代理
    """
    result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
    if len(result):
      return choice(result)
    else:
      result = self.db.zrevrange(REDIS_KEY, 0, 100)
      if len(result):
        return choice(result)
      else:
        raise PoolEmptyError

  def derease(self, proxy):
    """
    代理值减一分，小于最小值则删除
    :param proxy: 代理
    :return: 修改后的代理分数
    """
    score = self.db.zscore(REDIS_KEY, proxy)
    if score and score>MIN_SCORE:
      print("代理", proxy, "当前分数：", score,"减1")
      return self.db.zincrby(REDIS_KEY, -1, proxy)
    else:
      print("代理", proxy, "当前分数：", score, "移除")
      return self.db.zrem(REDIS_KEY, proxy)

  def exits(self, proxy):
    return not self.db.zscore(REDIS_KEY, proxy) == None

  def max(self, proxy):
    print("代理",proxy, "可用，设置为",MAX_SCORE)
    return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

  def count(self):
    return self.db.zcard(REDIS_KEY)

  def all(self):
    return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

  def batch(self, start=0, stop=1):
    return self.db.zrevrange(REDIS_KEY, start, stop-1)


if __name__ == "__main__":
  conn = RedisClient()
  result = conn.batch(666, 888)
  print(result)