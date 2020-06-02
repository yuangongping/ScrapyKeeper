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
    SCHEDULER_ID = ''                   # 项目调度任务id
    ROUND_ID = ''                       # 项目调度轮次id

    SEED_LIST = ''                      # 项目请求种子列表
    RETRY_TIMES = 1                     # 下载重复次数
    CONCURRENT_REQUESTS = 8             # 并发请求数
    DOWNLOAD_DELAY = 0.5                # 下载延迟时间
    DOWNLOAD_TIMEOUT = 180              # 下载超时时间
    DOWNLOAD_SPEED = 1024              # 下载速度

    DOWNLOAD_SIZE = 32                  # 单个文件下载最大的大小
    DNSCACHE_ENABLED = True             # 启用DNS内存缓存
    DNSCACHE_SIZE = 10000               # DNS内存缓存大小
    DNS_TIMEOUT = 60                    # DNS查询超时时间，以秒为单位
    MIDDLEWARES_PROXY_OPEN = False      # 是否开启ip代理
    MIDDLEWARES_PROXY_VALUE = '所有请求' # 启用代理方式
    MIDDLEWARES_PROXY_URL = 'http://10.5.9.119:5060/proxy_ip'  # 代理ip地址

    MYEXT_ENABLED = True                # 开启扩展
    IDLE_NUMBER = 60                    # 从爬虫redis空置等待时间 60 * 5 = 300秒
    LOG_LEVEL = 'INFO'                  # 日志等级
    RETRY_ENABLE = True                 # 允许下载失败重试

    DEPTH_LIMIT = 0                    # 允许抓取网站的最大深度。如果为零，则不施加限制
    CRAWL_RANGE_SUFFIX = ""            # 采集后缀过滤
    CRAWL_RANGE_DEEP_NUM = 3           # 采集层数过滤
    CRAWL_RANGE_SIZE_FILTERING = 50    # 站点过滤
    CRAWL_RANGE_URL_REGULAR = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"  # url正则过滤
    CRAWL_RANGE_PROTOCOL_FILTERING = "http,https"  # 协议过滤
    CRAWL_RANGE_MAX_PAGE = 100000      # 站点最大页面数量
    CRAWL_RANGE_SUBDOMAINS = 5         # 站点子域名数量

    DEPTH_PRIORIT = 0                  # 遍历方法，0为深度优先，-1为广度优先
    SUFFIX = 'html, shtml'             # 后缀模式
    AGREEMENT_TYPE = 'http, https'     # 协议类型
    REGULAR = ''                       # 正则表达式
    KEYWORD_CODE = ''                  # 关键代码
    KEYWORD = ''                       # 关键字
    KEYWORD_LOGIC = 'and'              # 关键字选项

    ALL_PAGE = 1                       # 全部页面
    TARGET_PAGE = 2                    # 目标页面存储
    REDIS_HOST = '172.16.13.22'        # redis地址
    REDIS_PORT = '6379'                # redis端口
    REDIS_TYPE = 'set'                 # redis类型
    MYSQL_HOST = '172.16.13.22'        # mysql地址
    MYSQL_DB = 'duocaiyunspider'       # mysql数据库名
    MYSQL_TABLE = ""                   # mysql表名
    MYSQL_USERNAME = "root"            # mysql用户名
    MYSQL_PASSWORD = 'root'            # mysql密码
    MYSQL_PORT = "3306"                # mysql端口

    STORAGE_TYPE = 3                   # 文件存储方式
    DIRS = 'D =//pythonWorkSpace//spider//test_debug//debug' # 本地存储路径
    FTP_IP = "http =//10.5.9.84:8084/fdfs/uploads"
    FTP_PORT = '3360'  # ftp端口号
    FTP_USERNAME = 'root'  # ftp用户名
    FTP_PASSWORD = "root"  # ftp密码
    FILE_UPLOAD_URL = 'http://172.16.119.13/dcy-file/fdfs/upload'  # 分布式存储文件上传接口
    DATABASE_IP = '172.16.13.22'  # 数据库ip
    DATABASE_PORT = '3360'  # 数据库端口
    DATABASE_USERNAME = 'root'  # 数据库用户名
    DATABASE_PASSWORD = 'root'  # 数据库密码
    DATABASE_DBNAME = 'duocaiyunDB'  # 数据库名
    DATABASE_TABLENAME = 'duocaiyun'  # 数据库表名

    DATA_CALLBACK_URL = "http://172.16.13.22:5060/data_storage"  # 数据回传url
    DATA_CALLBACK_SIZE = '300'  # 回传大小
    APP_KEY = ""  # APP
    ACCOUNT_LIST = ""  # 账号管理

    SCHEDULER_TYPE = 1  # 启动方式1手动 2 自动
    SCHEDULER_MOUNTH = None
    SCHEDULER_DAY = None
    SCHEDULER_HOUR = None  # 小时
    SCHEDULER_MINUTE = None  # 分钟
    SCHEDULER_DESCRIPTION = None

    SCHEDULER_PERSIST = False                                                 # 爬虫关闭，清除redis调度器和去重记录
    SCHEDULER_DUPEFILTER_KEY = '{}:dupefilter'.format(ROOT_PROJECT_NAME)      # 去重规则，在redis中保存时对应的key

    DEPTH_PRIORITY = 0                                                        # 遍历方法，0/-1为深度优先, 1广度优先
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'               # 深度优先必须对应设置
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'                 # 深度优先必须对应设置

    def set(self, key, val):
        if hasattr(self, key):
            if isinstance(val, (list, dict)):
                val = demjson.encode(val)
            setattr(self, key, val)
        else:
            raise KeyError('ScrapySettings Key Error: No key %s' % key)

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
