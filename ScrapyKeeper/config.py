#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2020-4-28 14:07
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com

# dev
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Clc372493@localhost:3306/sk'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@172.16.119.6:3306/scrapykeeper'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 30

EMAIL_SENDER = '952838607@qq.com'
EMAIL_AUTH_CODE = 'vufpldztjxhhbecb'

ES_URL = 'http://172.10.10.31:9200/'  # 存储日志的数据库地址
DATASTORAGENAME="duocaiyunspdier"
