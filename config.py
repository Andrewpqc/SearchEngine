# -*- coding:utf-8 -*-
"""
Search Engine
    配置文件
"""

import os

#项目的根目录设置
basedir=os.path.dirname(os.path.abspath(__file__))

"""
Search Engine:
    Config     :  配置基类
    DevConfig  :  开发环境配置类
    TestConfig :  测试环境配置类
    ProConfig  :  生产环境配置
    default    :  开发环境配置
"""



class Config (object):
    """
    配置基类：
       秘钥配置，数据库模式配置
    """
    SECRET_KEY=os.environ.get('SECRET_KEY') or "you_never_know"
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    """
    开发环境配置类：
        数据库URI配置
    """
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get("DEV_DATABASE_URL") or \
        "mysql+pymysql://root:pqc19960320@120.77.220.239:32770/Test"

config={
    "default":DevConfig
}