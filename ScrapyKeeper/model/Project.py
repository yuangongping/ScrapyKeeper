#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Project.py
# @Time    : 2020-4-29 14:50
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class Project(Base):
    __tablename__ = 'project'
    project_name = db.Column(db.String(100), unique=True)
    applicant = db.Column(db.String(100))            # 申请人
    developers = db.Column(db.String(100))           # 项目的开发者
    for_project = db.Column(db.String(100))          # 提出需求的项目
    project_name_zh = db.Column(db.String(100))        # 项目的备注
    category = db.Column(db.String(255))             # 分类
    is_msd = db.Column(db.SmallInteger)              # 是否是主从分布式爬虫 0 单机爬虫 1 分布式爬虫
    status = db.Column(db.String(50))                # 运行状态，运行中或则休眠
    input_value = db.Column(db.Text)          # 爬虫入口参数
    config = db.Column(db.Text)          # 数据库配置
