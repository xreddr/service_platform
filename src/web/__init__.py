import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth
bp = Blueprint('web', __name__, url_prefix='/')

query_var = '?'

@bp.route('/')
def index():
    return render_template('wsc/index.html', OPEN_REG=current_app.config['OPEN_REG'])

@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if request.form['login'] == 'reg':
            return render_template('wsc/reg.html', username=username, password=password)
        
        response = auth.login_user(username, password)
        if response['code'] == 0:
            return redirect(url_for('web.home_page'))


    return render_template('wsc/login.html', OPEN_REG=current_app.config['OPEN_REG'])

@bp.route('/logout', methods=('GET',))
def logout():
    auth.logout()
    return redirect(url_for('web.index'))

# CREATE

@bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pass = request.form['confirm_pass']

        if password == confirm_pass:

            return render_template('wsc/about.html')
        
    return render_template('wsc/reg.html')


@bp.route('/home')
def home_page():
    return render_template('wsc/about.html')