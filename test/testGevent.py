# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : testGevent.py
import time

from gevent import monkey;monkey.patch_all()
import gevent.pool

class SHIT:
    def one(self):
        print("one")
        time.sleep(1)
        print("one")

    def two(self):
        print("two")
        time.sleep(1)
        print("two")



    def three(self):
        print("three")
        time.sleep(1)
        print("three")

    def main(self):
        def miao(p):
            print("This is callback")

        pool = gevent.pool.Pool(100)
        pool.spawn(self.one)
        pool.spawn(self.two)
        pool.spawn(self.three)
        pool.apply_async(self.one)
        pool.apply_async(self.two, args=[], callback=miao)
        pool.apply_async(self.three)

        start_time = time.time()
        pool.join()
        pool.kill()
        print(time.time() - start_time)

    def mainmain(self):
        start_time = time.time()
        self.one()
        self.two()
        self.three()
        print(time.time() - start_time)

if __name__ == '__main__':
    shit = SHIT()
    shit.main()
    # shit.mainmain()