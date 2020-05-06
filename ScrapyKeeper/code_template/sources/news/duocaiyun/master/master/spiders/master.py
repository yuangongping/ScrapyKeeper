# -*- coding: utf-8 -*-
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider


class @@@@@@@@Spider(CrawlSpider):
    name = "$$$$$$$$_master_spider"
    start_urls = ['&&&&&&&&']

    url_prefix = '.'.join(start_urls[0].split('.')[1:])

    rules = [
        Rule(LinkExtractor(allow=(r'%s*' % url_prefix)), callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        if 'http' in response.url:
            item = @@@@@@@@Item()
            item['url'] = response.url
            yield item
