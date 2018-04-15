# -*- coding: utf-8 -*-
import scrapy
import json
from live.items import LiveItem


class ZhanqiSpider(scrapy.Spider):
    name = 'zhanqi'
    allowed_domains = ['zhanqi.tv']
    start_urls = ['http://www.zhanqi.tv/api/static/v2.1/live/list/20/1.json']

    base_url = 'http://www.zhanqi.tv/api/static/v2.1/live/list/20/'
    page_num = 1
    max_page_num = 50
    live_category = 'zhanqi'

    def parse(self, response):
        response_json = json.loads(response.text)
        message = response_json.get('message')
        if message == '':
            room_list = response_json.get('data').get('rooms')
            for room in room_list:
                item = LiveItem()
                item['rid'] = str(room.get('id'))
                item['nn'] = room.get('nickname')
                item['rn'] = room.get('title')
                item['category'] = room.get('gameName')
                item['url'] = 'https://www.zhanqi.tv/' + room.get('url')
                item['ol'] = room.get('online')
                item['preview'] = room.get('spic')
                item['live_category'] = self.live_category
                yield item

        self.page_num += 1
        if self.page_num <= self.max_page_num:
            yield response.follow(self.base_url + str(self.page_num) + '.json', callback=self.parse)
