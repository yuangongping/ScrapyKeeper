# -*- coding: utf-8 -*-
import json
import redis


class __ProjectNamecapitalize__MasterPipeline(object):
    def __init__(self, redis_host, redis_port):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_name = "{{root_project_name}}"

    @classmethod
    def from_crawler(cls, crawler):
        """
        功能: scrapy为我们访问settings提供了这样的一个方法，这里，
        我们需要从需要从settings.py文件中，文件中，取得数据库的URI和数据库名称
        """

        # redis的配置
        REDIS_HOST = crawler.settings.get('REDIS_HOST', None)
        REDIS_PORT = crawler.settings.get('REDIS_PORT', None)

        if all([REDIS_HOST, REDIS_PORT]):
            return cls(redis_host=REDIS_HOST, redis_port=REDIS_PORT)
        else:
            raise ValueError('No param_config Redis connection setting !'
                             ' settings.py 中 Redis 的连接信息未正确配置')

    def open_spider(self, spider):
        """
        爬虫一旦开启，就会实现这个方法，连接到数据库
        :param spider:
        :return:
        """
        try:
            self.rediscli = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
        except ConnectionError:
            raise ConnectionError('Cannot connect Redis ! 无法连接Redis')

    def close_spider(self, spider):
       pass

    def process_item(self, item, spider):
        """
        处理从列表页提取的详情页url Pipeline，找出在数据库里面不存在的，放进redis列表
        :param item: item对象
        :param spider: spider对象
        :return: item
        """
        info_urls = item.get('url')
        self.rediscli.sadd(self.redis_name, json.dumps({'url': info_urls}))
