import functools
import sqlite3
import werkzeug.exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth

bp = Blueprint('cookbook', __name__, url_prefix='cookbook')

@bp.route('/new', methods=('GET', 'POST'))
@auth.authorize_login
def new_recipe():
    return render_template('cookbook/new.html')