#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2020-4-28 14:07
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com

# dev
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cetc@2019@10.5.9.110:3306/scrapykeeper'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 600

EMAIL_SENDER = '952838607@qq.com'
EMAIL_AUTH_CODE = 'vufpldztjxhhbecb'

ES_URL = 'http://10.5.9.118:9200/'  # 存储日志的数据库地址
DATASTORAGENAME="duocaiyunspider"
# DATASTORAGENAME="duocaiyunspider_dataresource"
