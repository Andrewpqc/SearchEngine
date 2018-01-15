# -*- coding:utf-8 -*-
"""
提供主要服务的蓝图
"""
from flask import Blueprint
service=Blueprint("service",__name__,
                  template_folder='templates',static_folder='static')
from . import views,errors