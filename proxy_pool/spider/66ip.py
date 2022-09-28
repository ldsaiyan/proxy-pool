# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : 66ip.py
import re
import time
import logging

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Spider(object):
    def __init__(self):
        logger.info("[*] Hi,66ip")
        self.url = 'http://www.66ip.cn/mo.php'
        self.ip_port_pattern = re.compile(
            r"((?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))):(\d*)")
        self.result = []

    def get_data(self):
        try:
            data = requests.get(self.url).text
            ip_port_list = self.ip_port_pattern.findall(data)

            if not ip_port_list:
                raise Exception('empty')

        except Exception as e:
            logger.info("[-] Spider Crawl in 66ip error: {}".format(str(e)))
            return []

        return [{"type": "HTTP", "ip": ip, "port": port, "from": "66ip"} for ip,port in ip_port_list]

    def run(self):
        self.result.extend(self.get_data())
        time.sleep(2)


if __name__ == '__main__':
    spider = Spider()
    print(spider.get_data())