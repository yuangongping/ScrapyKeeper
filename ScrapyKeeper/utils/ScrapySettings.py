#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ScrapySettings.py
# @Time    : 2020-5-29 14:56
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
# scrapy 的 settings 处理
import demjson


class ScrapySettings():
    PROJECT_NAME = ''                   # 工程名
    ROOT_PROJECT_NAME = ''              # 总的项目名
    ROOT_PROJECT_NAME_ZH = ''           # 项目中文名称
    SEED_LIST = ''                      # 项目请求种子列表
    SCHEDULER_ID = ''                   # 项目调度任务id
    ROUND_ID = ''                       # 项目调度轮次id
    MIDDLEWARES_PROXY_OPEN = False      # 是否开启ip代理

    MYEXT_ENABLED = True                # 开启扩展
    IDLE_NUMBER = 60                    # 从爬虫redis空置等待时间 60 * 5 = 300秒

    LOG_LEVEL = 'INFO'                  # 日志等级
    RETRY_ENABLE = True                 # 允许下载失败重试
    RETRY_TIMES = 1                     # 下载失败重试次数

    CONCURRENT_REQUESTS = 8             # 并发请求数
    DOWNLOAD_DELAY = 0.5                # 下载延迟时间
    DOWNLOAD_TIMEOUT = 180              # 下载超时时间

    DNSCACHE_ENABLED = True             # 启用DNS内存缓存
    DNSCACHE_SIZE = 10000               # DNS内存缓存大小
    DNS_TIMEOUT = 60                    # DNS查询超时时间，以秒为单位

    DEPTH_LIMIT = 0                     # 允许抓取网站的最大深度。如果为零，则不施加限制

    REDIS_HOST = '10.5.9.87'            # redis地址
    REDIS_PORT = 6379                   # redis端口
    MYSQL_HOST = '10.5.9.110'           # mysql地址
    MYSQL_DB = 'duocaiyunspider_dataresource'        # mysql数据库名
    MYSQL_TABLE = ''                    # mysql表名
    MYSQL_USERNAME = 'root'             # mysql用户名
    MYSQL_PASSWORD = 'root'             # mysql密码
    MYSQL_PROT = '3306'                 # mysql端口

    DATA_CALLBACK_URL = ''              # 数据回传url
    DATA_CALLBACK_SIZE = 200            # 数据回传大小
    FILE_UPLOAD_URL = 'http://10.5.9.84:8084/dcy-file/fdfs/upload'            # 文件上传接口url
    PROXY_CENTER_URL = ''                                                     # 代理ip请求接口url

    SCHEDULER_PERSIST = False                                                 # 爬虫关闭，清除redis调度器和去重记录
    SCHEDULER_DUPEFILTER_KEY = '{}:dupefilter'.format(ROOT_PROJECT_NAME)      # 去重规则，在redis中保存时对应的key

    DEPTH_PRIORITY = 0                                                        # 遍历方法，0/-1为深度优先, 1广度优先
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'               # 深度优先必须对应设置
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'                 # 深度优先必须对应设置

    ACCOUNT_LIST = '[]'  # 账号管理

    def set(self, key, val):
        if hasattr(self, key):
            setattr(self, key, val)
        # else:
        #     raise KeyError('ScrapySettings Key Error: No key %s' % key)

    def load(self, txt: str = None, **kwargs):
        """  Load ScrapySettings from a json type string or a dict """
        if txt:
            try:
                dic = demjson.decode(txt)
            except Exception:
                raise SyntaxError('ScrapySettings load error: Wrong JSON Syntax')
            for k in dic:
                self.set(k, dic[k])

        for key in kwargs:
            self.set(key, kwargs[key])

    def dump(self, _to_dict=True):
        """ dump ScrapySettings to a json string """
        d = {}
        for prop in dir(self):
            if prop.isupper():
                d[prop] = getattr(self, prop)
        if _to_dict:
            return d
        return demjson.encode(d)
