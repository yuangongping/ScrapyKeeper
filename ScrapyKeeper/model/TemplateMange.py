#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model import db, Base


class TemplateMange(Base):
    __tablename__ = 'template'
    template_name = db.Column(db.String(100))           # 模板名称(news/weixin/weibo)
    template_type = db.Column(db.String(100))           # 模板类型(通用型新闻网页/新浪微博/微信公众号)
    crawl_url = db.Column(db.String(100), unique=True)  # 采集的url, 或者微博uuid, 或者微信号
    status = db.Column(db.String(100), default=1)       # 采集的url是否可添加为工程
