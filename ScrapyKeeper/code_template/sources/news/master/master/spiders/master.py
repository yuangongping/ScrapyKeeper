# -*- coding: utf-8 -*-
from ..items import __ProjectNamecapitalize__MasterItem
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import requests
import demjson
import scrapy


class __ProjectNamecapitalize__MasterSpider(CrawlSpider):
    name = "{{project_name}}_spider"
    project_name = "{{root_project_name}}"

    def start_requests(self):
        obj_project = requests.get(
            "http://172.16.13.22:5060/project?project_name={}&page_index=1&page_size=1".format(self.project_name),
            timeout=5
        ).text

        tpl_input = demjson.decode(obj_project)["data"]["data"][0]["tpl_input"]
        start_urls = tpl_input.get("start_urls")["value"].split(',')
        for url in start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_list
            )

    def parse_list(self, response):
        hrefs = response.xpath("//body//a").extract()
        for href in hrefs:
            href = response.urljoin(href)
            if 'http' in href:
                item = __ProjectNamecapitalize__MasterItem()
                item['url'] = href
                yield item
