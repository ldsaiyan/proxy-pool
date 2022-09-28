# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : testValidate.py
import time

import requests

def func1():
    yield 1
    yield from func2()
    yield 2

def func2():
    yield 3
    yield 4

if __name__ == '__main__':
    f1 = func1()
    for item in f1:
        print(item)
    request_begin = time.time()
    response_msg = requests.get(
        "http://httpbin.org/get?show_env=1&cur={}".format(request_begin),
        timeout=3
    ).json()
    print(request_begin)
    print(response_msg)
