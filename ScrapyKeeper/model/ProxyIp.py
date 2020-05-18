#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProxyIP.py
# @Time    : 2020-5-16 17:10
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class ProxyIpAgency(Base):
    """  代理IP提供商 """
    __tablename__ = 'proxy_ip_agency'
    agency_name = db.Column(db.String(255), comment='IP提供商')
    req_url = db.Column(db.String(255), comment='IP获取地址')
    req_num_per = db.Column(db.Integer, comment='每次请求获取ip的数量')
    req_num_max = db.Column(db.Integer, comment='IP最大获取数量')

    live_time = db.Column(db.Integer, comment='IP存活时间')
    method = db.Column(db.String(255), comment='IP提供商请求方法')
    params = db.Column(db.Text, comment='IP获取请求参数, 直接拼接到url中的参数')
    headers = db.Column(db.Text, comment='IP获取请求头')
    body = db.Column(db.Text, comment='IP获取请求体')


class ProxyIpRecord(Base):
    """
    代理IP获取记录表
    """
    __tablename__ = 'proxy_ip_record'
    req_url = db.Column(db.String(255), comment='请求获取代理IP的IP地址')
    agency_id = db.Column(db.String(255), comment='IP代理商的id')
    agency_name = db.Column(db.String(255), comment='IP代理商名称')
    req_project = db.Column(db.String(255), comment='请求获取代理IP的爬虫项目')
    req_num = db.Column(db.Integer, comment='本次获取IP的数量')
    live_seconds = db.Column(db.Integer, comment='本次IP的存活时间（秒）')


class ProxyIpCurrent(Base):
    __tablename__ = 'proxy_ip_current'
    ip = db.Column(db.String(50))  # ip
    port = db.Column(db.Integer)  # 端口

    @classmethod
    def empty_storage(cls):
        """
        清空数据库里面的数据
        :return:
        """
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def refresh_storage(cls, proxy_ip_list):
        """
        存储代理ip
        :param proxy_ip_list:
        :return:
        """
        # 先清空数据库
        cls.empty_storage()
        save_list = []
        for proxy_ip in proxy_ip_list:
            save_list.append(cls(ip=proxy_ip.get('ip'), port=proxy_ip.get('port')))

        db.session.add_all(save_list)
        db.session.commit()
