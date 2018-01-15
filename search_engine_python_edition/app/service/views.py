# -*- coding:utf-8 -*-
from flask import jsonify,request,render_template,abort
from . import service
from app.models import MovieInfo
from manage import shourcut_retriever
from app import db


@service.route('/',methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template('service/search.html')
    elif request.method=="POST":
        keywords=request.form.get("keywords")
        results=shourcut_retriever(keywords)
        for result in results:
            print(result[1])
        flag=True if len(results) else False
        return render_template("service/results.html",
                                            flag=flag,
                                            results=results)







