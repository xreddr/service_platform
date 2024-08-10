import functools
from flask import Blueprint, render_template

bp = Blueprint('web', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('wsc/index.html')

@bp.route('/login')
def login():
    return render_template('wsc/login.html')

@bp.route('/about')
def about_page():
    return render_template('wsc/about.html')