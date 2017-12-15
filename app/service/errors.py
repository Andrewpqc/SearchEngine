from . import service
from flask import render_template

@service.errorhandler(404)
def page_not_found(e):
    return render_template('service/404.html'),404

@service.errorhandler(500)
def internal_server_error(e):
    return render_template('service/500.html'),500