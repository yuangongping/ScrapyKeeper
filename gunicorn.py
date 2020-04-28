#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : gunicorn.py
# @Time    : 2020-4-28 14:17
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from gevent import monkey

monkey.patch_all()

import multiprocessing

debug = False
loglevel = 'debug'
bind = '127.0.0.1:5060'
pidfile = 'gunicorn.pid'
logfile = 'debug.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
