# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : storages.py
import ast
import logging

import redis

from setting import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY,INITIAL_SCORE,MIN_SCORE,MAX_SCORE

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RedisHandle(object):
    def __init__(self):
        # Why can't try except the connect
        logger.info("[*] Connecting to redis server")
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        # try:
        # except Exception as e:

    def init(self):
        pass

    def add(self, proxy):
        """
        Add proxy,and setting max score
        :param proxy: proxy
        :return:
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: INITIAL_SCORE})

    def all(self):
        """
        Get all proxy
        :return: all proxy
        """
        return [ast.literal_eval(proxy) for proxy in self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)]

    def exists(self, proxy):
        """
        Does the proxy exist
        :param proxy: proxy
        :return: true or false
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        Setting proxy MAX_SCORE
        :param proxy: proxy
        :return:
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY,{proxy: MAX_SCORE})

    def all_count(self):
        """
        Get all proxy count
        :return: count
        """
        return self.db.zcard(REDIS_KEY)

    def type_count(self,type):
        """
        Get all the same type proxy count
        :param type: type:
        :return: count
        """
        return len([proxy for proxy in self.all() if proxy['type'].lower() == type])

    def random(self,type):
        """
        Specify type，return top score
        :param type: type
        :return: proxy
        """
        _ = self.db.zrangebyscore(REDIS_KEY, INITIAL_SCORE, MAX_SCORE)
        max_score_proxy = [ast.literal_eval(proxy) for proxy in _]

        try:
            return [proxy for proxy in max_score_proxy if proxy['type'].lower() == type][0]
        except Exception as e:
            return "Sorry, there's no match"


    def decrease(self, proxy):
        """
        Score minus one，Delete if less than the minimum value
        :param proxy: proxy
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def get(self,type):
        http_proxy = []
        https_proxy = []
        # all_proxy = [ast.literal_eval(proxy) for proxy in self.all()]
        all_proxy = self.all()
        # switch
        for proxy in all_proxy:
            if proxy['type'] == 'HTTP':
                http_proxy.append(proxy)
            elif proxy['type'] == 'HTTPS':
                https_proxy.append(proxy)

        if type == 'http':
            return http_proxy
        elif type == 'https':
            return https_proxy

if __name__ == '__main__':
    pass
    # test
    # rh = RedisHandle()
    # rh.add("8.8.8.8:8888")
