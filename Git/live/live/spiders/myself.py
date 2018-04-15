# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class MyselfSpider(scrapy.Spider):
    name = 'myself'
    allowed_domains = ['39.106.146.64']
    start_urls = ['http://39.106.146.64/']

    category1 = ['douyu', 'panda', 'longzhu', 'zhanqi' 'yy', 'all']
    category2 = ['lol', 'dnf', 'lscs', 'jdqs', 'zj', 'hw', 'ms']

    def parse(self, response):
        for i in self.category1:
            for j in self.category2:
                for k in range(1, 6):
                    link = self.start_urls[0] + i + '/' + j + '/' + str(k)
                    request = Request(link, callback=self.print_url)
                    yield request

    def print_url(self, response):
        print('*' * 50)
        print(response.url)
