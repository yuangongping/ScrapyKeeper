#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : build_egg.py
# @Time    : 2020-5-21 9:44
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
# @contact : xie-hong-tao@qq.com
import glob
import os
import shutil
import sys
import tempfile
from subprocess import check_call

from scrapy.utils.conf import get_config
from scrapy.utils.python import retry_on_eintr


def build_egg(egg_name, source_dir, dest_dir=None):
    if not os.path.exists(os.path.join(source_dir, 'scrapy.cfg')):
        raise FileExistsError('scrapy.cfg is not exist')

    os.chdir(source_dir)
    if not os.path.exists('setup.py'):
        settings = get_config().get('settings', 'default')
        _create_default_setup_py(settings=settings)
    d = tempfile.mkdtemp(prefix="scrapydeploy-")
    o = open(os.path.join(d, "stdout"), "wb")
    e = open(os.path.join(d, "stderr"), "wb")
    retry_on_eintr(check_call, [sys.executable, 'setup.py', 'clean', '-a', 'bdist_egg', '-d', d],
                   stdout=o, stderr=e)
    o.close()
    e.close()
    egg = glob.glob(os.path.join(d, '*.egg'))[0]

    dest_dir = source_dir if dest_dir is None else dest_dir

    shutil.copyfile(egg, os.path.join(dest_dir, egg_name))


def _create_default_setup_py(**kwargs):
    _SETUP_PY_TEMPLATE = """
# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = %(settings)s']},
)
""".lstrip()
    with open('setup.py', 'w') as f:
        f.write(_SETUP_PY_TEMPLATE % kwargs)