# -*- coding: utf-8 -*-
from ..items import __ProjectNamecapitalize__Item
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class __ProjectNamecapitalize__Spider(CrawlSpider):
    name = "{{project_name}}_master_spider"
    start_urls = ["{{start_url}}"]

    url_prefix = '.'.join(start_urls[0].split('.')[1:])

    rules = [
        Rule(LinkExtractor(allow=(r'%s*' % url_prefix)), callback='parse_list')
    ]

    def parse_list(self, response):
        if 'http' in response.url:
            item = __ProjectNamecapitalize__Item()
            item['url'] = response.url
            yield item
