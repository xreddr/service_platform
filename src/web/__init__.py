import functools
from flask import Blueprint, render_template

bp = Blueprint('web', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/about')
def about_page():
    return render_template('about.html')