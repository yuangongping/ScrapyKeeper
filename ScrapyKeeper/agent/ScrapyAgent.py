#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ScrapyProxy.py
# @Time    : 2020-4-28 14:26
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import time
import socket
from typing import Dict

from scrapyd_api import ScrapydAPI


class ScrapyAgent(object):
    """ scrapy项目代理类 """
    def __init__(self, server_url):
        self.server_url = server_url
        self.scrapyd_api = ScrapydAPI(server_url)

    def __repr__(self):
        return '<ScrapyAgent %s>' % self.server_url

    @property
    def server(self):
        return self.server_url

    def list_projects(self):
        return self.scrapyd_api.list_projects()

    def del_project(self, project_name):
        try:
            return self.scrapyd_api.delete_project(project_name)
        except:
            return False

    def list_spiders(self, project_name):
        return self.scrapyd_api.list_spiders(project_name)

    def start_spider(self, project_name, spider_name):
        return self.scrapyd_api.schedule(project_name, spider_name)

    def cancel_spider(self, project_name, job_id):
        return self.scrapyd_api.cancel(project_name, job_id)

    def deploy(self, project_name: str, version: int, egg_byte: bytes) -> "Dict or bool":
        spider_num = self.scrapyd_api.add_version(project_name, version, egg_byte)
        return {
            'project': project_name,
            'version': version,
            'spiders': spider_num,
        } if spider_num else False

    def log_url(self, project_name, spider_name, job_id):
        return '{}/logs/{}/{}/{}'\
            .format(self.server_url, project_name, spider_name, job_id)