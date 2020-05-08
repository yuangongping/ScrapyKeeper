#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model import db, Base


class SendEmail(Base):
    __tablename__ = 'sendemail'
    project_name = db.Column(db.String(100))         # 项目名称
    project_id = db.Column(db.String(100))           # 项目id
    job_id = db.Column(db.String(100), unique=True)  # 任务调度id
    email = db.Column(db.String(100))      # 接收人邮箱
