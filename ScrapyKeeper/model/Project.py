#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Project.py
# @Time    : 2020-4-29 14:50
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from typing import Dict

from ScrapyKeeper.model import db, Base
from sqlalchemy.sql import exists
from sqlalchemy.exc import DataError


class Project(Base):
    __tablename__ = 'sk_project'
    project_name = db.Column(db.String(100), unique=True)
    applicant = db.Column(db.String(100))            # 申请人
    developers = db.Column(db.String(100))           # 项目的开发者
    for_project = db.Column(db.String(100))          # 提出需求的项目
    project_alias = db.Column(db.String(100))        # 项目的备注
    category = db.Column(db.String(255))             # 分类
    is_msd = db.Column(db.SmallInteger)              # 是否是主从分布式爬虫 0 单机爬虫 1 分布式爬虫
