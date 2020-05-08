# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import __ProjectNamecapitalize__DetailItem
from .mysql_db.tables import Content
from .mysql_db.operate import session
import logging
import requests


class __ProjectNamecapitalize__Pipeline(object):
    def __init__(self):
        self.batch_crawl_num = 0
        self.batch_file_size = 0

    def open_spider(self, spider):
        """
        爬虫一旦开启，就会实现这个方法，连接到数据库
        :param spider:
        :return:
        """
        try:
            self.session = session
        except ConnectionError:
            raise ConnectionError('Cannot connect MYSQL ! 无法连接MYSQL')

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        """
        功能: 数据清洗并保存每个实现保存的类里面必须都要有这个方法,且名字固定, 用来具体实现怎么保存
        :param item: item对象
        :param spider: spider对象
        :return: item
        """
        try:
            # 如果为详情页的item，则保存数据至mysql
            if isinstance(item, __ProjectNamecapitalize__DetailItem):
                obj = Content()
                for k, v in item.items():
                    setattr(obj, k, v)
                self.session.add(obj)
                self.session.commit()
                self.batch_crawl_num += 1
                self.batch_file_size += item.get("file_size")
            """每存储50条数据， 向数据存储接口发送一个请求"""
            if self.batch_crawl_num == 50:
                requests.post("http://172.16.119.6:5060/data_storage", data={
                    "project_name": "{{project_name}}",
                    "project_alias": "{{project_name_zh}}",
                    "num": 50,
                    "file_size": self.batch_file_size
                })
                # 发送请求后, 计数重置
                self.batch_crawl_num = 0
                self.batch_file_size = 0
        except Exception as e:
            logging.error("数据存储错误！", e)
            self.session.rollback()
