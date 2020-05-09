# -*- coding: utf-8 -*-
from ..items import __ProjectNamecapitalize__MasterItem
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import requests
import json


class __ProjectNamecapitalize__MasterSpider(CrawlSpider):
    name = "{{project_name}}_spider"
    project_name = "{{root_project_name}}"
    urls = requests.get("http://127.0.0.1:5060/start_urls?status={}".format(project_name)).text
    start_urls = json.loads(urls)["data"]

    url_prefix = '.'.join(start_urls[0].split('.')[1:])

    rules = [
        Rule(LinkExtractor(allow=(r'%s*' % url_prefix)), callback='parse_list')
    ]

    def parse_list(self, response):
        if 'http' in response.url:
            item = __ProjectNamecapitalize__MasterItem()
            item['url'] = response.url
            yield item
