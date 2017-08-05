# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hospital.items import HospitalItem
from hospital.models.config import DBSession
from hospital.models.model import Log
from scrapy.conf import settings


class A36dsjSpider(CrawlSpider):
    name = 'a36dsj'
    allowed_domains = ['www.36dsj.com']
    start_urls = ['http://www.36dsj.com/archives/category/application-area/large-medical-data',
                  ]
    settings.overrides['DOWNLOAD_TIMEOUT'] = 5
    settings.overrides['CONCURRENT_REQUESTS'] = 32
    DOWNLOAD_DELAY = 0.5
    rules = (
        Rule(LinkExtractor(allow=r'.*/page/\d+', restrict_xpaths="//div[@class='pagination']"), follow=True),
        Rule(LinkExtractor(allow=r'.*/archives/\d+', restrict_xpaths="//div[@class='content']"),
             callback='parse_item', follow=True),
        # Rule(SgmlLinkExtractor(allow='26062.html', restrict_xpaths="//article"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = HospitalItem()
        item['url'] = response.xpath("//h1[@class='article-title']/a/@href").extract_first().strip().encode('utf-8')
        session = DBSession()
        if len(item['url']) == 0 or session.query(Log).filter(Log.url == item['url']).count():
            session.close()
        else:
            item['title'] = response.xpath(
                "//h1[@class='article-title']/a/text()").extract_first().strip().encode(
                'utf-8')
            item['content'] = response.xpath("//article/node()").extract()
            item['domain'] = 'www.36dsj.com'
            session.close()
            return item
