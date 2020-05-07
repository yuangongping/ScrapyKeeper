# -*- coding: utf-8 -*-
from ..items import __ProjectNamecapitalize__MasterItem
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class __ProjectNamecapitalize__MasterSpider(CrawlSpider):
    name = "{{project_name}}_spider"
    start_urls = ["{{start_url}}"]

    url_prefix = '.'.join(start_urls[0].split('.')[1:])

    rules = [
        Rule(LinkExtractor(allow=(r'%s*' % url_prefix)), callback='parse_list')
    ]

    def parse_list(self, response):
        if 'http' in response.url:
            item = __ProjectNamecapitalize__MasterItem()
            item['url'] = response.url
            yield item
