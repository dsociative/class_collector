#!/usr/bin/env python

from setuptools import setup

setup(name='class_collector',
      description='socket server for flash client',
      author='dsociative',
      author_email='admin@geektech.ru',
      py_modules=['class_collector'],
#      package_dir={'class_collector': 'class_collector.py'},
      install_requires = ['import_file']
     )
