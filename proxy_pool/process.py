# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : process.py
import os
import time
import logging

from gevent import monkey;monkey.patch_all()
import gevent.pool
import requests

from proxy_pool.utils import load_object
from proxy_pool.storages import RedisHandle

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProxyPool(object):
    def __init__(self):
        pass

    def init(self):
        logger.info("[*] Init")
        self.spiders = []
        self.proxies = []
        self.valid_proxies = []

        self.pool = gevent.pool.Pool(100)
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.spider_name = os.listdir(os.path.join(self.base_dir, 'spider'))
        self.module_spider_path = "proxy_pool.spider."
        self.rh = RedisHandle()


    def load_spider(self):
        logger.info("[*] Load spider")
        for spider in self.spider_name:
            if os.path.splitext(spider)[1] != '.py' or spider == '__init__.py':
                continue

            try:
                # self.module_spider_path => proxy_pool.spider.
                # os.path.splitext(spider)[0] => 89ip
                cls = load_object(self.module_spider_path + os.path.splitext(spider)[0],'Spider')
            except Exception as e:
                logger.info("[-] Load spider {} error: {}".format(spider, str(e)))
                continue

            instance = cls()
            # inst.proxies = copy.deepcopy(self.valid_proxies)
            self.spiders.append(instance)

    def crawl_proxies(self):
        logger.info("[*] Crawl proxies")
        for spider in self.spiders:
            self.pool.spawn(spider.run)

        # start_time = time.time()
        self.pool.join()
        self.pool.kill()
        # print(time.time() - start_time)
        self._collect_result()

    def _collect_result(self):
        for spider in self.spiders:
            self.proxies.extend(spider.result)


        # test for see
        for proxy in self.proxies:
            print(proxy)


    def validate_proxy(self):
        logger.info("[*] Validate proxy")
        for proxy in self.proxies:
            if proxy.get('type') == 'HTTP' or proxy.get('type') == 'http':
                self.pool.apply_async(self._validate_proxy, args=(proxy, 'http'), callback=lambda x: self.valid_proxies.append(x) if x else None )
            elif proxy.get('type') == 'HTTPS' or proxy.get('type') == 'https':
                self.pool.apply_async(self._validate_proxy, args=(proxy, 'https'), callback=lambda x: self.valid_proxies.append(x) if x else None)

        self.pool.join()
        self.pool.kill()

        logger.info("[*] Check {} proxies, Got {} valid proxies".format(len(self.proxies), len(self.valid_proxies)))


    def put_in_storage(self):
        logger.info("[*] Put in Storage")
        # test for see
        for proxy in self.valid_proxies:
            print(proxy)
            # here add data to redis
            self.rh.add(str(proxy))

        logger.info("[*] Put {} proxies into the storage.".format(len(self.valid_proxies)))


    def _validate_proxy(self,proxy,scheme):
        ip = proxy.get('ip')
        port = proxy.get('port')
        request_proxies = {
            scheme: "{}:{}".format(ip, port)
        }

        request_begin = time.time()
        try:
            #print("start")
            #print(request_proxies)
            response_msg = requests.get(
                "{}://httpbin.org/get?show_env=1&cur={}".format(scheme, request_begin),
                proxies=request_proxies,
                timeout=8
            ).json()
            #print("end")
        except:
            return
        request_end = time.time()

        test = response_msg.get('origin', '').split(', ')
        #print(response_msg.get('origin', ''))


        return {
            "type": scheme,
            "ip": ip,
            "port": port,
            "response_time": round(request_end - request_begin, 3),
            "test": test,
            "from": proxy.get('from')
        }

    def db_validate_proxy(self):
        logger.info("[*] db validate proxy")
        # print(self.rh.all())
        for proxy in self.rh.all():
            #print(ast.literal_eval(proxy))
            # if ast.literal_eval(proxy).get('type') == 'HTTP' or ast.literal_eval(proxy).get('type') == 'http':
            #     self.pool.apply_async(self._validate_proxy, args=(ast.literal_eval(proxy), 'http'),
            #                           callback=lambda x: self.rh.max(proxy) if x else self.rh.decrease(proxy))
            # elif ast.literal_eval(proxy).get('type') == 'HTTPS' or ast.literal_eval(proxy).get('type') == 'https':
            #     self.pool.apply_async(self._validate_proxy, args=(ast.literal_eval(proxy), 'https'),
            #                           callback=lambda x: self.rh.max(proxy) if x else self.rh.decrease(proxy))
            #print(proxy)

            if proxy['type'] == 'HTTP' or proxy['type'] == 'http':
                self.pool.apply_async(self._validate_proxy, args=(proxy, 'http'),
                                      callback=lambda x: self.rh.max(str(proxy)) if x else self.rh.decrease(str(proxy)))
            elif proxy['type'] == 'HTTPS' or proxy['type'] == 'https':
                self.pool.apply_async(self._validate_proxy, args=(proxy, 'https'),
                                      callback=lambda x: self.rh.max(str(proxy)) if x else self.rh.decrease(str(proxy)))

            self.pool.join()
            self.pool.kill()

        logger.info("[*] Check {} proxies.".format(self.rh.all_count()))

    def start_server(self):
        pass

    def run(self):
        self.init()
        self.db_validate_proxy()
        self.load_spider()
        self.crawl_proxies()
        self.validate_proxy()
        self.put_in_storage()

if __name__ == '__main__':
    gp = ProxyPool()
    gp.run()
    # pass

    # test
    #gp.load_spider()
