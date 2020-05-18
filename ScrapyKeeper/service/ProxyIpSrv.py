#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProxyIPSrv.py
# @Time    : 2020-5-16 17:18
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import json
import random
import time
import demjson

import requests
from urllib.parse import urlencode

from flask import request
from flask_restful import abort

from ScrapyKeeper import lock
from ScrapyKeeper.model.ProxyIp import ProxyIpCurrent, ProxyIpAgency, ProxyIpRecord

from ScrapyKeeper.service import BaseSrv


class ProxyIpSrv(BaseSrv):
    """"""
    def list_to_dict(self, data: list):
        d = {}
        for item in data:
            d[item['key']] = item['value']
        return d

    def request_ip(self, url, method, params: list = None, headers: list = None, body: list = None):
        """
        发出请求从IP服务提供商获取IP
        :param url: 请求地址
        :param method: 请求方法
        :param params: 拼接url的参数
        :param headers: 请求头
        :param body: 请求体
        :return:
        """
        if len(params) > 1:  # 如果有需要将请求参数拼接到url中就拼接url
            req_url = "%s?%s" % (url, urlencode(self.list_to_dict(params)))
        else:
            req_url = url

        print('-----   req url ', req_url)

        if method == 'GET':  # 如果是get请求
            response = requests.get(req_url, headers=self.list_to_dict(headers))
        else:  # post 请求
            response = requests.post(req_url, data=json.dumps(self.list_to_dict(body)), headers=self.list_to_dict(headers))

        if response.status_code == 200:
            result = json.loads(response.text)
            return result

    def get_ip(self, **kwargs):
        with lock:
            req_time = kwargs['timestamp']
            if len(str(req_time)) > 10:
                abort(400, message="Timestamp is second type (length = 10)")

            get_num = kwargs['get_num']
            req_project = kwargs['project']

            # 最后一次代理IP请求数据
            last_record = ProxyIpRecord.query.order_by(ProxyIpRecord.id.desc()).limit(1).scalar()

            ip_expire_time = 0  # 上一次ip的过期时间
            if last_record:
                # 最后一次代理IP获取的时间
                last_ip_record_time = int(last_record.date_created.timestamp())
                system_nowtime = int(time.time())
                # 系统的时间和请求的时间不能相差太大
                if abs(system_nowtime - req_time) > 30:
                    abort(400, message="Timestamp faraway  传入的时间和系统时间相差太大")

                last_live_seconds = int(last_record.live_seconds)
                ip_expire_time = last_ip_record_time + last_live_seconds

            # 如果请求P的时间 大于 IP的过期时间 表明当前数据库IP已经失效，请求新的IP
            if ip_expire_time < req_time:
                agencies = ProxyIpAgency.all(_to_dict=False)
                agency = random.choice(agencies)

                res = self.request_ip(url=agency.req_url,
                                      method=agency.method,
                                      params=demjson.decode(agency.params),
                                      headers=demjson.decode(agency.headers),
                                      body=demjson.decode(agency.body)
                                      )

                if res is not None:
                    live_seconds = agency.live_time  # 获取新ip代理商的ip存活时间
                    # 刷新存储代理IP的数据库数据
                    ProxyIpCurrent.refresh_storage(res['data'])
                    # 添加IP请求数据
                    req_ip = request.remote_addr
                    # 获取IP代理商的每次请求ip数量参数
                    get_num = get_num if get_num else int(agency.get_num)
                    ProxyIpRecord.save({
                        "req_url": req_ip,
                        "agency_name": agency.agency_name,
                        "agency_id": agency.id,
                        "req_project": req_project,
                        "live_seconds": live_seconds,
                        "req_num": get_num
                    })

                    res['proxy_expire_time'] = int(time.time()) + live_seconds
                return res
