# -*- coding: utf-8 -*-
import scrapy
import json
from live.items import LiveItem


class PandaSpider(scrapy.Spider):
    name = 'panda'
    allowed_domains = ['panda.tv']
    start_urls = ['https://www.panda.tv/live_lists?status=2&token=&pagenum=120&order=top&pageno=1']

    base_url = 'https://www.panda.tv/live_lists?status=2&token=&pagenum=120&order=top&pageno='
    page_num = 1
    max_page_num = 20
    live_category = 'panda'

    def parse(self, response):
        response_json = json.loads(response.text)
        errno = response_json.get('errno')
        if errno == 0:
            room_list = response_json.get('data').get('items')
            for room in room_list:
                item = LiveItem()
                item['rid'] = str(room.get('id'))
                item['nn'] = room.get('userinfo').get('nickName')
                item['rn'] = room.get('name')
                item['category'] = room.get('classification').get('cname')
                if item['category'] == '户外直播':
                    item['category'] = '户外'
                item['url'] = 'https://www.panda.tv/' + room.get('id')
                item['ol'] = room.get('person_num')
                item['preview'] = room.get('pictures').get('img')
                item['live_category'] = self.live_category
                yield item

        self.page_num += 1
        if self.page_num <= self.max_page_num:
            yield response.follow(self.base_url + str(self.page_num), callback=self.parse)
