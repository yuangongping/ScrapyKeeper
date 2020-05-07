# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()


class Content(Base):
    __tablename__ = '{{root_project_name}}'
    __table_args__ = {'comment': '{{project_name_zh}}'}
    id = Column(Integer, autoincrement=True, primary_key=True, comment='id')
    collect_date = Column(DateTime, default=datetime.datetime.now, comment='数据采集时间')

    title = Column(String(255), comment='文章标题')
    keyword = Column(String(255), comment='关键字', default="")
    abstract = Column(Text, comment='描述或者摘要', default="")
    author = Column(String(255), comment='作者', default="")
    source = Column(String(255), comment='文章来源, 若文章详情页（列表页）都无来源，则以采集的网站为来源')

    body = Column(Text, comment='文章正文')
    type = Column(String(255), comment='类型', default="文稿")
    create_time = Column(DateTime,  comment='发布时间')

    url = Column(String(512), unique=True, index=True, comment='新闻原文网址')
    "上传至文件系统后返回的uuid"
    file_group = Column(Text, comment='文件列表')





