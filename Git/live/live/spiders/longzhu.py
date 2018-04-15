# -*- coding: utf-8 -*-
import scrapy
import json
from live.items import LiveItem


class LongzhuSpider(scrapy.Spider):
    name = 'longzhu'
    allowed_domains = ['longzhu.com']
    start_urls = ['http://api.longzhu.com/tga/streams?max-results=18&sort-by=views&start-index=0']

    base_url = 'http://api.longzhu.com/tga/streams?max-results=18&sort-by=views&start-index='
    page_num = 1
    max_page_num = 100
    live_category = 'longzhu'

    def parse(self, response):
        response_json = json.loads(response.text)

        room_list = response_json.get('data').get('items')
        for room in room_list:
            item = LiveItem()
            channel = room.get('channel')
            item['rid'] = str(channel.get('id'))
            item['nn'] = channel.get('name')
            item['rn'] = channel.get('status')
            item['category'] = room.get('game')[0].get('name')
            if item['category'] == '地下城与勇士':
                item['category'] = 'DNF'
            if item['category'] == '主机游戏（综合）':
                item['category'] = '主机游戏'
            item['url'] = channel.get('url')
            item['ol'] = room.get('viewers')
            item['preview'] = room.get('preview')
            item['live_category'] = self.live_category
            yield item

        self.page_num += 1
        if self.page_num <= self.max_page_num:
            yield response.follow(self.base_url + str(self.page_num * 18 - 1), callback=self.parse)
