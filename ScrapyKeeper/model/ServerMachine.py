#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Server.py
# @Time    : 2020-4-28 14:58
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from sqlalchemy import and_

from ScrapyKeeper.model import db, Base


class ServerMachine(Base):
    __tabelename__ = 'sk_server_machine'
    url = db.Column(db.String(50), primary_key=True)
    status = db.Column(db.SmallInteger, default=1)  # 1启动 0禁用
    is_master = db.Column(db.SmallInteger, primary_key=True)  # 1主 2从

    @classmethod
    def master_url(cls):
        sm = cls.query.filter(and_(cls.status == 1, cls.is_master == 1)).first()
        return sm.url if sm is not None else None

    @classmethod
    def slave_urls(cls):
        sms = cls.query.filter(and_(cls.status == 1, cls.is_master == 0)).all()
        return [sm.url for sm in sms]

    @classmethod
    def save(cls, dic: dict) -> "Dict or None":

        machine = ServerMachine()
        machine.set(dic)

        if machine.id is not None :
            item = cls.find_by_id(machine.id, _to_dict=False)
            if item is None:
                raise ValueError('Table %s has no data where id %s' % (cls.__table__, machine.id))
            else:
                # 改变主键了
                if item.url != machine.url or item.is_master != machine.is_master:
                    exit_machine = cls.query.filter(
                        and_(cls.url == machine.url, cls.is_master == machine.is_master)).first()
                    if exit_machine is not None:
                        _type = '主服务器' if machine.is_master == 1 else '从服务器'
                        raise ValueError('已经存在地址为 %s 的 %s' % (dic['url'], _type))

                item.set(dic)
                dic = item.to_dict()
        else:
            exit_machine = cls.query.filter(and_(cls.url == machine.url, cls.is_master == machine.is_master)).first()
            if exit_machine is not None:
                _type = '主服务器' if machine.is_master == 1 else '从服务器'
                raise ValueError('已经存在地址为 %s 的 %s' % (machine.url, _type))
            else:
                new_one = cls()
                new_one.set(dic)
                db.session.add(new_one)
        db.session.commit()
        return dic
