#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import requests
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model import db
from flask_restful import abort


class ServerMachineSrv(object):
    @classmethod
    def save(cls, url: str, is_master: int, status: int):
        """
        功能:　添加服务器
        :return: 成功返回success, 失败返回相应的异常
        """

        try:

            # 判断添加的服务器是否可用
            res = requests.get(url, timeout=1)
            if res.status_code == 200:
                # 保存数据
                ServerMachine.save()
                obj = ServerMachine(
                    url=url,
                    status=status,
                    is_master=is_master
                )

            else:
                abort(400, message='Server machine disabled 服务器不可用')
        except Exception as e:
            abort(500, message='Save server machine failed')

    @classmethod
    def list(cls):
        """
        功能: 列出所有的服务器
        :return: 成功返回服务器信息列表,url,is_master,status三个字段的信息, data的值格式如下:
                 [
                 {'url':'http://172.10.10.184:6800',
                 'is_master': '0',
                 'status': '1'}
                 ]
                 失败则返回空列表
        """
        try:
            machines = ServerMachine.query.all()
            data = []
            for machine in machines:
                machine_dict = machine.to_dict()
                data.append(machine_dict)
            return data
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @classmethod
    def edit(cls, url: str, is_master: int, status: int):
        """
        功能: 编辑服务器的信息
        :return: 成功返回'data': 'success', 失败'data': 'error'
        """
        try:
            # 判断服务器是否可用
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                machine = ServerMachine.query.filter_by(url=url).first()
                machine.url = url
                machine.is_master = is_master
                machine.status = status
                db.session.commit()
                return machine.to_dict
            else:
                abort(500, 'machine unused')
        except Exception as e:
            abort(400, 'edit machines fail: %s' % e)

    @classmethod
    def delete(cls, url: str):
        """
        功能: 删除服务器的信息
        :return: 成功返回'data': 'success', 失败'data': 'error'
        """
        try:
            machine = ServerMachine.query.filter_by(url=url).first()
            if machine:
                db.session.delete(machine)
                db.session.commit()
        except Exception as e:
            abort(400, 'delete machine fail')
