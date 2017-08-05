# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from hospital.models.config import DBSession
from hospital.models.model import Hit, Log
from scrapy.exceptions import DropItem

class HitPipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        if spider.name in ['hit','hc3i', 'a36dsj']:
            hit = Hit(title=item['title'], content=''.join(item['content']).encode('utf-8'), url=item['url'],
                      domain=item['domain'])
            self.session.add(hit)
            log = Log(url=item['url'])
            self.session.add(log)
            self.session.commit()
        else:
            return item

    def close_spider(self, spider):
        self.session.close()


class CountDropPipeline(object):
    def __init__(self):
        self.count = 1

    def process_item(self, item, spider):
        if self.count == 0:
            raise DropItem("Over item found: %s" % item)
        else:
            self.count -= 1
        return item

