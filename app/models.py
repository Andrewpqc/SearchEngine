'''
models:
    Movies 包含所有电影信息
'''
from app import db
class Movies(db.Model):
    __tablename__ = "requirements"
    __table_args__ = {"mysql_charset": "utf8"}
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(200))
    pinginfo_id=db.Column(db.Integer,db.ForeignKey("pinginfos.id"))


