#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import requests
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper import db
from flask import abort
from ScrapyKeeper import agent


class ParamConfigSrv(object):
    @classmethod
    def add_machine(cls, ip: str, is_master: int, status: int):
        """
        功能:　添加服务器
        :return: 成功返回success, 失败返回相应的异常
        """
        machine = ServerMachine.query.filter_by(ip=ip).first()
        if machine is None:
            try:
                obj = ServerMachine(
                    ip=ip,
                    status=status,
                    is_master=is_master
                )
                res = requests.get(ip, timeout=1)
                if res.status_code == 200:
                    # 保存数据
                    db.session.add(obj)
                    db.session.commit()
                    agent.regist(ScrapydProxy(ip), is_master)
                else:
                    abort(500, 'machine unused')
            except Exception as e:
                abort(400, 'add machine failed')
        else:
            abort(400, 'machine existed')

    @classmethod
    def list_machine(cls):
        """
        功能: 列出所有的服务器
        :return: 成功返回服务器信息列表,ip,is_master,status三个字段的信息, data的值格式如下:
                 [
                 {'ip':'http://172.10.10.184:6800',
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
    def edit_machine(cls, id: int, ip: str, is_master: int, status: int):
        """
        功能: 编辑服务器的信息
        :return: 成功返回'data': 'success', 失败'data': 'error'
        """
        try:
            # 判断服务器是否可用
            res = requests.get(ip, timeout=2)
        except:
            abort(400, 'machine unused')
        try:
            if res.status_code == 200:
                machine = ServerMachine.query.filter_by(id=id).first()
                """先删除"""
                if machine:
                    machine_dict = machine.to_dict()
                    if machine_dict.get('is_master') == '1':
                        for master_machine_instance in agent.spider_service_instances_master:
                            if master_machine_instance._server == machine.ip:
                                agent.spider_service_instances_master.remove(master_machine_instance)
                    else:
                        for slave_machine_instance in agent.spider_service_instances_slave:
                            if slave_machine_instance._server == machine.ip:
                                agent.spider_service_instances_slave.remove(slave_machine_instance)
                    # 删除数据库里的值
                    db.session.delete(machine)
                    db.session.commit()

                """保存数据"""
                obj = ServerMachine(
                    ip=ip,
                    status=status,
                    is_master=is_master
                )
                # 保存数据
                db.session.add(obj)
                db.session.commit()
                agent.regist(ScrapydProxy(ip), is_master)
        except Exception as e:
            abort(400, 'edit machines fail: %s' % e)

    @classmethod
    def delete_machine(cls, id: int):
        """
        功能: 删除服务器的信息
        :return: 成功返回'data': 'success', 失败'data': 'error'
        """
        try:
            machine = ServerMachine.query.filter_by(id=id).first()
            if machine:
                db.session.delete(machine)
                db.session.commit()
                machine_dict = machine.to_dict()
                if machine_dict.get('is_master') == '1':
                    for master_machine_instance in agent.spider_service_instances_master:
                        if master_machine_instance._server == machine.ip:
                            agent.spider_service_instances_master.remove(master_machine_instance)
                else:
                    for slave_machine_instance in agent.spider_service_instances_slave:
                        if slave_machine_instance._server == machine.ip:
                            agent.spider_service_instances_slave.remove(slave_machine_instance)
        except Exception as e:
            abort(400, 'delete machine fail')
