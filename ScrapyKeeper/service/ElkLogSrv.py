#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import os
import time
from elasticsearch import Elasticsearch
from flask import abort
from ScrapyKeeper import app


class ElkLogSrv(object):
    @classmethod
    def es_connection(cls):
        """ 连接elasticsearch数据库 """
        try:
            es_url = app.config.get('ES_URL')
            es_connection = Elasticsearch(hosts=[es_url])
            return es_connection
        except Exception as e:
            abort(400, 'Elasticsearch connect fail: %s' % e)

    @classmethod
    def log_messages(cls, project_name: str = None, page: int = 1, page_size: int = 5):
        """
        根据项目分页查找该项目的错误日志信息
        :param project_name:  项目名称
        :param page: 页码
        :param page_size: 每页显示多少条
        :return: 返回对应页的错误日志信息
        """
        if not project_name:
            return None
        # 操作elasticsearch数据库的执行语句
        # 主要是按照项目名称查询所有的错误日志
        query_json = {
            "size": page_size,  # 控制获取数据量
            "from": (page-1) * page_size,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "loglevel.keyword": "ERROR"  # 查询条件语句
                            }
                        },
                        {
                            "term": {
                                "project_name.keyword": project_name  # 查询条件语句
                            }
                        }
                    ]
                }
            },
            "sort": {
                "time": {
                    "order": "desc"
                }
            }
        }
        # 筛选需要获取的字段
        source = ["project_name", "loglevel", "time", "type", "messages"]
        connection = cls.es_connection()  # 连接数据库
        # 从数据库中提取数据
        es_query = connection.search(index='duocaiyun-*', body=query_json, _source=source)
        es_data = es_query['hits']['hits']
        if not es_data:
            return None
        # 递归出现错误的详细数据及字段, 提取需要的数据
        messages = []
        for data in es_data:
            messages.append(data['_source'])

        return messages

    @classmethod
    def log_count(cls):
        """
       计算各项目的错误日志数, 用于提示哪些项目有错误日志, 错误日志数大于0的项目将有预警标识
       :return: [
                    {
                      "key" : "bid_master",
                      "doc_count" : 804
                    },
                    {
                      "key" : "rmrb_rmrbhwb",
                      "doc_count" : 52
                    }
              ]
       """
        # 操作elasticsearch数据库的执行语句
        # 主要是按照项目名称分组计数
        try:
            query_json = {
                "size": 0,  # 控制获取数据量
                "query": {
                    "term": {
                        "loglevel.keyword": "ERROR"  # 查询条件语句
                    }
                },
                "aggs": {  # 分组聚合
                    "project_group": {
                        "terms": {
                            "field": "project_name.keyword"
                        }
                    }
                }
            }
            connection = cls.es_connection()  # 连接数据库
            # 从数据库中提取数据
            es_data = connection.search(index='duocaiyun-*', body=query_json)
            if es_data:
                # 获取分组聚合的各项目出现错误的数量
                return es_data.get('aggregations').get('project_group').get('buckets')
            else:
                return None
        except:
            return None

    @classmethod
    def log_delete(cls, project_name: str):
        """
        处理项目日志: 删除数据库与收集本地日志中已被处理过得日志
        :return:
        """
        # 操作elasticsearch数据库的执行语句
        # 按照项目名称及时间删除已被处理过得日志
        query_json = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "project_name.keyword": project_name
                            }
                        },
                        {
                            "range": {
                                 "time": {
                                    "lte": time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 小于某个日期
                                 }
                            }
                        }
                    ]
                }
            }
        }
        connection = cls.es_connection()  # 连接数据库

        try:
            # 同时从数据库中删除数据
            connection.delete_by_query(index='duocaiyun-*', body=query_json)
            return True

        except Exception as e:
            abort(400, '%s logs delete fail: %s' % (project_name, e))




