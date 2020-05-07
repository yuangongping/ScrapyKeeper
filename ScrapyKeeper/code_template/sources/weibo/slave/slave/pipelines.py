# -*- coding: utf-8 -*-
import redis
import json
from .items import __ProjectNamecapitalize__SlavePostItem
from .mysql_db.tables import Post, Comment
from .mysql_db.operate import session
import logging
import requests


class __ProjectNamecapitalize__SlavePipeline(object):
    def __init__(self, redis_host, redis_port):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_name = "{{root_project_name}}"
        self.batch_crawl_num = 0
        self.batch_file_size = 0

    @classmethod
    def from_crawler(cls, crawler):
        # redis的配置
        REDIS_HOST = crawler.settings.get('REDIS_HOST', None)
        REDIS_PORT = crawler.settings.get('REDIS_PORT', None)

        if all([REDIS_HOST, REDIS_PORT]):
            return cls(redis_host=REDIS_HOST, redis_port=REDIS_PORT)
        else:
            raise ValueError('No param_config Redis connection setting !'
                             ' settings.py 中 Redis 的连接信息未正确配置')

    def open_spider(self, spider):
        try:
            self.rediscli = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
            self.session = session
        except ConnectionError:
            raise ConnectionError('Cannot connect Redis & MYSQL ! 无法连接Redis和MYSQL')

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        try:
            # 如果为详情页的item，则保存数据至mysql， 同时向redis数据库的详情页集合中添加记录， 用于去重
            if isinstance(item, __ProjectNamecapitalize__SlavePostItem):
                obj_instance = Post()
            else:
                obj_instance = Comment()
            for k, v in item.items():
                setattr(obj_instance, k, v)
            self.session.add(obj_instance)
            self.session.commit()
            self.batch_crawl_num += 1
            self.batch_file_size += item.get("file_size")
            """每存储200条数据， 向数据存储接口发送一个请求"""
            if self.batch_crawl_num == 200:
                requests.post("http://172.16.119.6:5060/data_storage", data={
                    "project_name": "weiboceshi_slave",
                    "project_alias": "微博测试",
                    "num": 50,
                    "file_size": self.batch_file_size
                })
                # 发送请求后, 计数重置
                self.batch_crawl_num = 0
                self.batch_file_size = 0
        except Exception as e:
            logging.error("数据存储错误！", e)
            self.session.rollback()
