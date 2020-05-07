# -*- coding: utf-8 -*-
from scrapy import signals
import random
from scrapy.utils.project import get_project_settings
import logging
import time
import json
import requests


class __ProjectNamecapitalize__SlaveProxyMiddleware(object):
    """换代理IP"""
    settings = get_project_settings()
    proxy_list = []
    proxy_expire_time = 0

    def process_request(self, request, spider):
        now_timestamp = int(time.time())
        # 如果代理IP的过期时间小于当前的时间, 证明IP已过期，请求刷新IP
        if self.proxy_expire_time < now_timestamp:
            params = {
                'timestamp': now_timestamp,
                'project': get_project_settings().get('PROJECT_NAME'),
            }
            response = json.loads(requests.get(url=self.settings.get('PROXY_CENTER_URL'), params=params).text)
            if response['code'] >= 400:
                logging.ERROR('[ReFresh ProxyIp ERROR] %s !' % response['msg'])
            else:
                self.proxy_list = response['data']
                self.proxy_expire_time = response['proxy_expire_time']
                logging.info('[Success Refresh ProxyIp] %s ! Total %s , Expire time %s'
                             % (response['msg'], len(self.proxy_list),
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.proxy_expire_time))))

        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = 'http://%s:%s' % (proxy['ip'], proxy['port'])


class __ProjectNamecapitalize__SlaveSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class __ProjectNamecapitalize__SlaveDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

