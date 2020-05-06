# -*- coding: utf-8 -*-
from ..items import *
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
import json
from ..mysql_db.operate import session
from ..mysql_db.tables import Content
from ..utils.extractor import Extractor
from ..utils.tools import upload, unify_date
import requests
from urllib.parse import urlparse


class @@@@@@@@SlaveSpider(RedisSpider):
    name = "$$$$$$$$_slave_spider"
    redis_key = "$$$$$$$$"
    session = session
    gne_extract = Extractor()

    def make_request_from_data(self, data):
        """
        重写RedisCrawlSpider中的该算法, 以实现更多参数的传递
        :param data: redis数据库中获取的数据
        :return:
        """
        # 从redis数据库中获取详情页的url
        redis_data = json.loads(bytes_to_str(data, self.redis_encoding))
        url = redis_data.get('url')
        "在mysql中查询"
        exist = self.session.query(Content).filter_by(url=url).first()
        if not exist:
            return scrapy.Request(
                url=str(url),
                callback=self.parse
            )

    def parse(self, response):
        result = self.gne_extract.extract(response.text)
        detailItem = @@@@@@@@DetailItem()
        detailItem["title"] = result['title']
        detailItem["author"] = result['author']
        detailItem["source"] = "人民网"

        detailItem["body"] = result['content']
        detailItem["type"] = "文稿"
        detailItem["create_time"] = unify_date(result['publish_time'])

        detailItem["url"] = response.url
        "上传至文件系统后返回的uuid"
        uuid_list = []
        img_urls = result['images']
        imgs_size = 0
        for img_url in img_urls:
            img_url = response.urljoin(img_url)
            img_body = requests.get(url=img_url).content  # 请求附件url
            imgs_size += int(len(img_body) / 1024) # 单位kb
            uuid = upload(response.urljoin(img_body))
            if uuid:
                uuid_list.append(uuid)

        detailItem["file_size"] = imgs_size
        detailItem["file_group"] = json.dumps(uuid_list)
        yield detailItem

        all_a = response.xpath("//body//a/@href").extract()
        for href in all_a:
            href = response.urljoin(href.strip())
            if urlparse(href).netloc in href:
                item = @@@@@@@@Item()
                item['url'] = href
                yield item
