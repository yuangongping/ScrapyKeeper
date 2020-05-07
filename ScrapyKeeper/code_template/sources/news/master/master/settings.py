# -*- coding: utf-8 -*-
BOT_NAME = '{{project_name}}'

SPIDER_MODULES = ['{{project_name}}.spiders']
NEWSPIDER_MODULE = '{{project_name}}.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
   # 'master.middlewares.UserAgent': 1,
   # 'master.middlewares.MasterDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
   '{{project_name}}.pipelines.__ProjectNamecapitalize__MasterPipeline': 300,
}

# scrapy-redis 配置
REDIS_HOST = '172.16.119.6'
REDIS_PORT = 6379
# 去重类，要使用Bloom Filter请替换DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# # 散列函数的个数，默认为6，可以自行修改
BLOOMFILTER_HASH_NUMBER = 6
# # Bloom Filter的bit5数，默认30，2^30 = 10亿位=10亿/8 字节=128MB空间，去重量级1亿
BLOOMFILTER_BIT = 25
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"



