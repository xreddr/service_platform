import functools
import sqlite3
import werkzeug.exceptions
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, flash, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth

bp = Blueprint('cookbook', __name__, url_prefix='cookbook')

@bp.route('/new', methods=('GET', 'POST'))
@auth.authorize_login
def new_recipe():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['recipe']
        keywords = request.form['keywords'].split(',')
        keywords_string = json.dumps(keywords)
        user_id = session.get('user_id')
        print(title)
        print(body)
        print(type(keywords), type(keywords_string))
        print(keywords_string)
        print(user_id)
        # conn = db.lite_conn()
        # cur = conn.cursor()
        flash('button pressed!')

    return render_template('cookbook/new.html')