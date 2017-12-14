from flask import jsonify,Response
from . import service
from app.models import Movies
from manage import crawl
from app import db
import json

@service.route('/simpleping')
def index():
   pass






