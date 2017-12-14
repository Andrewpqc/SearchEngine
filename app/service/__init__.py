"""
提供主要服务的蓝图
"""
from flask import Blueprint
service=Blueprint("service",__name__)
from . import views