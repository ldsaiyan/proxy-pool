# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : testStorages.py

def testStorages():
    from proxy_pool.storages import RedisHandle

    rh = RedisHandle()
    test_data = "{'type': 'http', 'ip': '192.168.1.1', 'port': '3128', 'response_time': 8.807, 'test': ['192.168.1.1', '192.168.1.2'], 'from': 'ip3366'}"
    test_type = "http"

    print("add: ", rh.add(test_data))
    print("get all: ", rh.all())
    print("exists: ", rh.exists(test_data))
    print("max: ", rh.max(test_data))
    print("all_count: ", rh.all_count())
    print("type_count: ", rh.type_count(test_type))
    print("random: ", rh.random(test_type))
    print("decrease: ", rh.decrease(test_data))
    print("get type all: ", rh.get(test_type))

if __name__ == '__main__':
    testStorages()