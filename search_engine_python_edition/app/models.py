#-*- coding:utf-8 -*-
'''
models:
    MovieInfo 包含所有电影信息

'''
from app import db

class MovieInfo(db.Model):
    """
    表名：movieinfo
    字段：
        　id 自增id
       　url 该电影页面所对应的url
      　　name 电影名
  　　　　director 导演
        Screenwriter 编剧
        actor 主演
        type 类型
        country 国家
        displaytime 上映时间
        othername 别名
        score 评分
        shortcut 简介
    """
    __tablename__ = "movieinfo"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.BigInteger,primary_key=True)
    url=db.Column(db.String(100))
    name=db.Column(db.String(200))
    direcotr=db.Column(db.String(500))
    Screenwriter=db.Column(db.String(1000))
    actor=db.Column(db.String(1000))
    type=db.Column(db.String(500))
    country=db.Column(db.String(500))
    displaytime=db.Column(db.String(500))
    othername=db.Column(db.String(500))
    score=db.Column(db.Float)
    shortcut=db.Column(db.Text)