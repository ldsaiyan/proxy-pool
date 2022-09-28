# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : utils.py
import importlib

import requests

def load_object(module,name):
    mod = importlib.import_module(module)
    # print(mod)

    try:
        class_name = getattr(mod,name)
    except AttributeError:
        raise NameError("Module {} doesn't define any Class named {}".format(mod,name))

    # print(class_name)
    return class_name

def check():
    pass

def alive():
    headers = {'user-agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    proxy = {}

    rp = requests.get('https://www.baidu.com/',proxies=proxy,headers=headers,timeout=3)
    if rp.status_code == 200:
        return 200