import functools
import sqlite3
import werkzeug.exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth




bp = Blueprint('web', __name__, url_prefix='/')
from . import cookbook
bp.register_blueprint(cookbook.bp)
from . import chatter
bp.register_blueprint(chatter.bp)


@bp.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if request.form['login'] == 'reg':
                return render_template('wsc/reg.html', username=username, password=password)
        except werkzeug.exceptions.BadRequestKeyError:
            pass
        response = auth.login_user(username, password)
        print(response['code'])
        if response['code'] == 0:
            return redirect(url_for('web.home_page'))
        
    return render_template('wsc/index.html', OPEN_REG=current_app.config['OPEN_REG'], ADMIN_CODE=current_app.config['ADMIN_CODE'])


@bp.route('/logout', methods=('GET',))
def logout():
    auth.logout()
    return redirect(url_for('web.index'))

# CREATE

@bp.route('/register', methods=('POST', 'GET'))
@auth.open_reg_required
def register():
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pass = request.form['confirm_pass']
        role = request.form.get('role')
        if role == 'admin':
            role = auth.get_role_id('admin')
            print(role['body'])
            role_id = role['body']
        else:
            role = auth.get_role_id('user')
            print(role['body'])
            role_id = role['body']

        if password == confirm_pass:
            try:
                reg = auth.register_user(username, password, role_id)
            except sqlite3.IntegrityError:
                reg = {'code': 0}
            print(reg['code'])
            if reg['code'] == 0:
                logged = auth.login_user(username, password)
                print(logged['code'])
                if logged['code'] == 0:
                    return render_template('wsc/home.html')
        
    return render_template('wsc/reg.html')


@bp.route('/home')
@auth.authorize_login
def home_page():
    db.close_db()
    try:
        conn = db.lite_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM service;")
        services = cur.fetchall()
    except all as e:
        services = e

    return render_template('wsc/home.html', services=services)

@bp.route('manage_users', methods=('GET', 'POST'))
@auth.authorize_login
def manage_user_page():
    conn = db.lite_conn()
    cur = conn.cursor()
    user_list = cur.execute("SELECT * FROM user WHERE role_id = ?;", (3,)).fetchall()
    admin_list = cur.execute("SELECT * FROM user WHERE role_id = ?;", (2,)).fetchall()

    return render_template('wsc/manage_users.html', user_list=user_list, admin_list=admin_list)

@bp.route('/cookbook', methods=('GET', 'POST'))
@auth.authorize_login
def cookbook():
    db.close_db()
    conn = db.lite_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipe WHERE user_id = ?;", (session['user_id'],))
    recipes = cur.fetchall()
    cur.execute("SELECT * FROM recipe_keyword WHERE user_id = ?;", (session['user_id'],))
    keywords = cur.fetchall()
    cur.execute("SELECT * FROM cookbook_category WHERE user_id = ?;", (session['user_id'],))
    categories = cur.fetchall()
    cur.close()
    db.close_db()
    return render_template('cookbook/home.html', recipes=recipes, keywords=keywords, categories=categories)

@bp.route('/chatter')
@auth.authorize_login
def chatter_page():
    return render_template('chatter/home.html')

@bp.route('/db_dump')
@auth.authorize_login
def db_dump():
    db.upload_blob()
    return redirect(url_for('web.home_page'))