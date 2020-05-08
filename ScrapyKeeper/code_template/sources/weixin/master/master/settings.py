# -*- coding: utf-8 -*-


BOT_NAME = '{{project_name}}'

SPIDER_MODULES = ['{{project_name}}.spiders']
NEWSPIDER_MODULE = '{{project_name}}.spiders'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 8

ITEM_PIPELINES = {
   '{{project_name}}.pipelines.__ProjectNamecapitalize__Pipeline': 300,
}


