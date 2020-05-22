#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model import db, Base


class SendEmail(Base):
    __tablename__ = 'sendemail'
    round_id = db.Column(db.String(100), unique=True)  # 轮次id
    email = db.Column(db.String(100))      # 接收人邮箱
    title = db.Column(db.String(255))
    content = db.Column(db.Text)


    @classmethod
    def find_by_round(cls, round_id) -> "SendEmail":
        return cls.query.filter(cls.round_id == round_id).first()

