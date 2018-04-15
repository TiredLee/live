# -*- coding: utf-8 -*-
import scrapy
import json
from live.items import LiveItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyu.com']
    start_urls = ['https://www.douyu.com/gapi/rkc/directory/0_0/1']

    base_url = 'https://www.douyu.com/gapi/rkc/directory/0_0/'
    page_num = 1
    max_page_num = 20
    live_category = 'douyu'

    def parse(self, response):
        response_json = json.loads(response.text)
        status = response_json.get('msg')
        if status == 'success':
            room_list = response_json.get('data').get('rl')
            for room in room_list:
                item = LiveItem()
                item['rid'] = str(room.get('rid'))
                item['nn'] = room.get('nn')
                item['rn'] = room.get('rn')
                item['category'] = room.get('c2name')
                item['url'] = 'https://www.douyu.com' + room.get('url')
                item['ol'] = room.get('ol')
                item['preview'] = room.get('rs1')
                item['live_category'] = self.live_category
                yield item

        self.page_num += 1
        if self.page_num <= self.max_page_num:
            yield response.follow(self.base_url + str(self.page_num), callback=self.parse)
