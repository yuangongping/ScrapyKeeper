# -*- coding: utf-8 -*-
from ..items import *


class {{project_name_capitalize}}Spider(scrapy.Spider):
    name = "{{project_name}}_master_spider"
    url = "{{start_url}}"

    def start_requests(self):
        """
        功能: 发出初始页面的请求
        :return:
        """
        yield scrapy.Request(
            url=self.url,
            callback=self.parse,
        )

    def parse(self, response):
        all_a = response.xpath("//body//a/@href").extract()
        for href in all_a:
            if "java" in href:
               continue
            href = response.urljoin(href.strip())
            if 'http' in href:
                item = {{project_name_capitalize}}Item()
                item['url'] = href
                yield item
