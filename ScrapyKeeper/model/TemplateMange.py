#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model import db, Base


class TemplateMange(Base):
    __tablename__ = 'template'
    # 模板名称（英文|模板路径索引）
    tpl_name = db.Column(db.String(100))
    # 模板名称（中文）
    tpl_zh = db.Column(db.String(100))
    # 采集的url, 或者微博uuid, 或者微信号
    tpl_type = db.Column(db.SmallInteger)
    # 模板输入
    tpl_input = db.Column(db.Text)
    # 模板图标
    tpl_img = db.Column(db.LargeBinary(65536))
