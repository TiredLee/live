# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rid = scrapy.Field()
    rn = scrapy.Field()
    nn = scrapy.Field()
    ol = scrapy.Field()
    preview = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    live_category = scrapy.Field()

