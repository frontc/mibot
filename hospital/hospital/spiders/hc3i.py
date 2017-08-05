# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hospital.items import HospitalItem
from hospital.models.config import DBSession
from hospital.models.model import Log


class Hc3iSpider(CrawlSpider):
    name = 'hc3i'
    allowed_domains = ['news.hc3i.cn']
    start_urls = ['http://news.hc3i.cn/col/304',
                  'http://news.hc3i.cn/col/305',
                  'http://news.hc3i.cn/col/307',
                  'http://news.hc3i.cn/col/310'
                  ]
    DOWNLOAD_DELAY = 0.5
    rules = (
        Rule(LinkExtractor(allow=r'.*/list_\d+_\d.htm', restrict_xpaths="//div[@class='page']"), follow=True),
        Rule(LinkExtractor(allow=r'.*art/\d+/\d+.htm', restrict_xpaths="//div[@class='article']"), callback='parse_item', follow=True),
        # Rule(SgmlLinkExtractor(allow='26062.html', restrict_xpaths="//article"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = HospitalItem()
        item['url'] = response.url.strip().encode('utf-8')
        session = DBSession()
        if len(item['url']) == 0 or session.query(Log).filter(Log.url == item['url']).count():
            session.close()
        else:
            item['title'] = response.xpath("//div[@class='article']/div[@class='title']/text()").extract_first().strip().encode(
                'utf-8')
            item['content'] = response.xpath("//div[@class='article']/div[@class='answer']/node()").extract()
            item['domain'] = 'news.hc3i.cn'
            session.close()
            return item