# -*- coding:utf-8 -*-
from flask import jsonify,request,render_template
from . import service
from app.models import MovieInfo
from manage import retriever
from app import db


@service.route('/',methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template('service/search.html')
    elif request.method=="POST":
        keywords=request.form.get("keywords")
        shortcuts=retriever(keywords)
        flag=True if len(shortcuts) else False
        return render_template("service/results.html",flag=flag,results=shortcuts)
        # return jsonify(shortcuts)






