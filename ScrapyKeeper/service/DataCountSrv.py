#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model.DataCount import DataCount
from flask_restful import abort


class DataCountSrv(object):
    @classmethod
    def save(cls, args: dict):
        """
        功能:　添加统计数据采集量
        :return: 成功返回success, 失败返回相应的异常
        """
        try:
            # 保存数据
            DataCount.save(args)
        except Exception as e:
            abort(500, message='Save data count failed')
