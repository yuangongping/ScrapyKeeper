#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : dev.py
# @Time    : 2020-4-28 13:51
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import os
import sys
sys.path.append(os.getcwd())
from ScrapyKeeper import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5060, debug=True, threaded=True)
