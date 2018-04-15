# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json

from live.items import LiveItem


class YySpider(scrapy.Spider):
    name = 'yy'
    allowed_domains = ['yy.com']
    start_urls = ['http://www.yy.com/catalog']
    live_category = 'yy'
    # http://www.yy.com/more/page.action?biz=chicken&subBiz=jdqs&page=2&moduleId=1473&pageSize=60

    def parse(self, response):
        category_list = response.xpath('/html/body/div[3]/div/div/div/div[2]/div/ul/li')
        for i in category_list:
            url = 'http://www.yy.com' + i.xpath('./a/@href').extract_first()
            category = i.xpath('./a/span[2]/text()').extract_first()
            request = Request(url, callback=self.list_room)
            request.meta['category'] = category
            yield request

    def list_room(self, response):
        html_text = response.text
        page_bar = re.findall(r'pageBar: {(.+)}', html_text)
        dict1 = {}
        if page_bar:
            for message in page_bar[0].split(', '):
                key, value = message.split(':')
                dict1[key] = value.strip('\'')

        if dict1:
            for page_num in range(1, int(dict1['totalPages']) + 1):
                url = 'http://www.yy.com/more/page.action?biz=%s&subBiz=%s&page=%s&moduleId=%s&pageSize=60' % (
                    dict1['biz'],
                    dict1['subBiz'],
                    str(page_num),
                    dict1['moduleId']
                )
                request = Request(url, callback=self.room_json)
                request.meta['category'] = response.meta['category']
                yield request

    def room_json(self, response):
        response_json = json.loads(response.text)
        result_code = response_json.get('resultCode')

        if result_code == 0:
            room_list = response_json.get('data').get('data')
            for room in room_list:
                item = LiveItem()
                item['rid'] = str(room.get('id'))
                item['nn'] = room.get('name')
                item['rn'] = room.get('desc')
                item['category'] = response.meta['category']
                if item['category'] == 'LOL':
                    item['category'] = '英雄联盟'
                item['url'] = 'http://www.yy.com' + room.get('liveUrl')
                item['ol'] = room.get('users')
                item['preview'] = room.get('thumb')
                item['live_category'] = self.live_category
                yield item

