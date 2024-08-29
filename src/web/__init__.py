import functools
import werkzeug.exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth
bp = Blueprint('web', __name__, url_prefix='/')


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
    # if not current_app.config['OPEN_REG'] and g.user['role'] != current_app.config['ADMIN_CODE']:
    #     return redirect(url_for('web.index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pass = request.form['confirm_pass']

        if password == confirm_pass:
            reg = auth.register_user(username, password)
            print(reg['code'])
            if reg['code'] == 0:
                logged = auth.login_user(username, password)
                print(logged['code'])
                if logged['code'] == 0:
                    return render_template('wsc/about.html')
        
    return render_template('wsc/reg.html')


@bp.route('/home')
def home_page():
    return render_template('wsc/about.html')