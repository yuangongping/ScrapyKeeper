#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from elasticsearch import Elasticsearch
from flask import abort


class LogManageSrv(object):
    @classmethod
    def es_connection(cls):
        try:
            es_connection = Elasticsearch(hosts=['http://172.10.10.31:9200/'])
            return es_connection
        except Exception as e:
            abort(400, 'Elasticsearch connect fail: %s' % e)

    @classmethod
    def log_messages(cls, project_name: str = None, page: int = 1, page_size: int = 5):
        if not project_name:
            return None
        # 操作elasticsearch数据库的执行语句
        # 主要是按照项目名称分组计数并查询所有的错误日志
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
            }
        }
        # 筛选需要获取的字段
        source = ["project_name", "loglevel", "time", "type", "messages"]
        connection = cls.es_connection()  # 连接数据库
        # 从数据库中提取数据
        es_query = connection.search(index='_all', body=query_json, _source=source)
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
        # 操作elasticsearch数据库的执行语句
        # 主要是按照项目名称分组计数并查询所有的错误日志
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
        es_data = connection.search(index='_all', body=query_json)
        # 获取分组聚合的各项目出现错误的数量
        '''
        [
            {
              "key" : "bid_master",
              "doc_count" : 804
            },
            {
              "key" : "rmrb_rmrbhwb",
              "doc_count" : 52
            }
      ]'''
        return es_data['aggregations']['project_group']['buckets']


