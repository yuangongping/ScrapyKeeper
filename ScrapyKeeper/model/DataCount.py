#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model import db, Base


class DataCount(Base):
    __tablename__ = 'sk_data_count'
    project_name = db.Column(db.String(255))  # 工程名 **必须与上传到爬虫平台的英文工程名同名
    developers = db.Column(db.String(255))
    address = db.Column(db.String(255))
    db_name = db.Column(db.String(255))
    table_name = db.Column(db.String(255))
    number = db.Column(db.String(255))
    image_number = db.Column(db.String(255))
    video_number = db.Column(db.String(255))
    audio_number = db.Column(db.String(255))
    file_number = db.Column(db.String(255))
    image_size = db.Column(db.String(255))
    video_size = db.Column(db.String(255))
    audio_size = db.Column(db.String(255))
    file_size = db.Column(db.String(255))
