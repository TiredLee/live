# -*- coding: utf-8 -*-
import pymysql


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MysqlPipeline(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='live',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        cols, values = zip(*item.items())
        sql = ("INSERT INTO room (%s) VALUES (%s)" %
               (','.join(cols), ','.join(['%s'] * len(cols))))
        try:
            self.cur.execute(sql, values)
        except Exception as e:
            print(e)
        self.conn.commit()
        return item
