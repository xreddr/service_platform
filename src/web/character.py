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
from datetime import datetime, timedelta, timezone


bp = Blueprint('character', __name__, url_prefix='character')


@bp.route('/', methods=['GET', 'POST'])
@auth.authorize_login
def load_char():
    now = datetime.now(timezone.utc)
    last_press = session.get("last_press", None)
    total_time = None

    if last_press:
        start_time = datetime.fromisoformat(last_press)
        total_time = int((now-start_time).total_seconds())/60

        session.pop("last_press", None)

    return render_template("character/home.html", total_time=total_time)

@bp.route('/record_press', methods=['GET', 'POST'])
@auth.authorize_login
def record_press():
    now = datetime.now(timezone.utc).isoformat()
    session["last_press"] = now
    return jsonify({"saved_time": now})