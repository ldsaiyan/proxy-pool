# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : ip3366.py
import re
import time
import logging

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Spider(object):
    def __init__(self):
        logger.info("[*] Hi,ip3366")
        page = 1
        self.url = "http://www.ip3366.net/?page={}".format(page)
        self.ip_port_pattern = re.compile(
            r"((?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9])))\<\/td\>\s+\<td\>(\d*)\<\/td\>\s+\<td\>.*\<\/td\>\s+\<td\>(\w*)\<\/td\>")
        self.result = []

    def get_data(self):
        try:
            data = requests.get(self.url).text
            ip_port_list = self.ip_port_pattern.findall(data)

            if not ip_port_list:
                raise Exception('empty')

        except Exception as e:
            logger.info("[-] Spider Crawl in ip3366 error: {}".format(str(e)))
            return []

        return [{"type": type, "ip": ip, "port": port, "from": "ip3366"} for ip,port,type in ip_port_list]
        # for i in ip_port_list:
        #     print(i)

    def run(self):
        self.result.extend(self.get_data())
        time.sleep(2)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    for i in spider.result:
        print(i)