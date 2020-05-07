# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()


class Post(Base):
    __tablename__ = "sinaweibo_weiboceshi"
    __table_args__ = {'comment': '新浪微博_微博测试'}
    Id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.now, comment='数据采集时间')
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                           comment='数据更新时间')
    publish_time = Column(String(255), comment="发送时间")
    repost_count = Column(String(64), comment="转发数")
    like_count = Column(String(64), comment="点赞数")
    comment_count = Column(String(64), comment="评论数")

    url = Column(String(512), unique=True, comment="帖子地址")
    publisher = Column(String(255), comment="发帖人")

    source = Column(String(255), comment="采集来源，如新浪微博的人民日报")
    publisher_url = Column(String(512), comment="发帖人微博地址")
    content = Column(Text, comment="微博内容")
    "上传至文件系统后返回的uuid"
    file_group = Column(Text, comment='文件列表')


class Comment(Base):
    __tablename__ = "sinaweibo_weiboceshi_comment"
    __table_args__ = {'comment': '新浪微博评论信息_微博测试'}
    Id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.now, comment='数据采集时间')
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                           comment='数据更新时间')

    content_uuid = Column(String(255), comment="评论id, 用于去重")
    post_url = Column(String(255), comment="评论的帖子url")
    name = Column(String(255), comment="评论人昵称")
    name_url = Column(String(255), comment="评论人微博主页地址")
    content = Column(Text, comment="评论的内容")
    comment_object = Column(String(255), comment="评论对象， 如果为空，则回复的是帖子，否则为指定的人昵称")
    comment_object_url = Column(String(255), comment="评论对象的微博主页地址")
    date = Column(String(255), comment="评论发表时间")
    like_num = Column(Integer, comment="评论被赞次数")

