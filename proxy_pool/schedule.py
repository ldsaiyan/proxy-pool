# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : schedule.py
import time

import schedule

from proxy_pool.process import ProxyPool
from setting import HOUR

def job():
    ProxyPool().run()
    #print("Hello")



def runSchedule():
    job()
    schedule.every(HOUR).hours.do(job)
    #schedule.every(10).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
