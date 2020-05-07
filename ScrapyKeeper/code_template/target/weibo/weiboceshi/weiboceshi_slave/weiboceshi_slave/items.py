# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field

class WeiboceshiSlavePostItem(scrapy.Item):
    publish_time = Field()
    repost_count = Field()
    like_count = Field()
    comment_count = Field()
    url = Field()
    publisher = Field()
    source = Field()
    publisher_url = Field()
    content = Field()
    "上传至文件系统后返回的uuid"
    file_group = scrapy.Field()

    file_size = scrapy.Field()


class WeiboceshiSlaveCommentItem(scrapy.Item):
    content_uuid = scrapy.Field()
    post_url = scrapy.Field()
    name = scrapy.Field()
    name_url = scrapy.Field()
    content = scrapy.Field()
    comment_object = scrapy.Field()
    comment_object_url = scrapy.Field()
    date = scrapy.Field()
    like_num = scrapy.Field()


