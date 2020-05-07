# -*- coding: utf-8 -*-
from ..items import CeershiMasterItem
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class CeershiMasterSpider(CrawlSpider):
    name = "ceershi_master_spider"
    start_urls = ["http://politics.people.com.cn/n1/2020/0429/c1001-31693461.html"]

    url_prefix = '.'.join(start_urls[0].split('.')[1:])

    rules = [
        Rule(LinkExtractor(allow=(r'%s*' % url_prefix)), callback='parse_list')
    ]

    def parse_list(self, response):
        if 'http' in response.url:
            item = CeershiMasterItem()
            item['url'] = response.url
            yield item

