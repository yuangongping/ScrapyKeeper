# -*- coding: utf-8 -*-
import scrapy


class {{project_name_capitalize}}Item(scrapy.Item):
    url = scrapy.Field()


class {{project_name_capitalize}}DetailItem(scrapy.Item):
    title = scrapy.Field()
    keyword = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()

    body = scrapy.Field()
    type = scrapy.Field()
    create_time = scrapy.Field()

    url = scrapy.Field()
    "上传至文件系统后返回的uuid"
    file_group = scrapy.Field()

    file_size = scrapy.Field()
