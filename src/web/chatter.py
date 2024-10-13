import functools
import sqlite3
import werkzeug.exceptions
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, flash, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth

bp = Blueprint('chatter', __name__, url_prefix='chatter')

'''
CREATE
'''


# POST

@bp.route('/new_post', methods=('GET', 'POST'))
@auth.authorize_login
def new_post():
    return redirect(url_for('web.home'))

# COMMENT

@bp.route('/new_comment', methods=('GET', 'POST'))
@auth.authorize_login
def new_comment():
    return redirect(url_for('web.home'))

'''
READ
'''


# POST

@bp.route('/read_post', methods=('GET', 'POST'))
@auth.authorize_login
def read_post():
    return redirect(url_for('web.home'))

# COMMENT

@bp.route('/read_comment', methods=('GET', 'POST'))
@auth.authorize_login
def read_comment():
    return redirect(url_for('web.home'))

'''
UPDATE
'''


# POST

@bp.route('/update_post', methods=('GET', 'POST'))
@auth.authorize_login
def update_post():
    return redirect(url_for('web.home'))

# COMMENT

@bp.route('/update_comment', methods=('GET', 'POST'))
@auth.authorize_login
def update_comment():
    return redirect(url_for('web.home'))

'''
DELETE
'''


# POST

@bp.route('/delete_post', methods=('GET', 'POST'))
@auth.authorize_login
def delete_post():
    return redirect(url_for('web.home'))

# COMMENT

@bp.route('/delete_comment', methods=('GET', 'POST'))
@auth.authorize_login
def delete_comment():
    return redirect(url_for('web.home'))