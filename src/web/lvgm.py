import functools
import sqlite3
import werkzeug.exceptions
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, flash, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth
# CKEditor
from flask import Flask
from flask_ckeditor import CKEditor
# Calendar
from datetime import datetime, timedelta

current_app.config.update(CKEDITOR_SERVE_LOCAL='ON', CKEDITOR_HEIGHT=400)
ckeditor = CKEditor(current_app)


bp = Blueprint('lvgm', __name__, url_prefix='lvgm')

@bp.route('/', methods=['GET', 'POST'])
@auth.authorize_login
def lvgm_home():
    return render_template('lvgm/base.html')