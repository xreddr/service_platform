import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, session, url_for, current_app, g, redirect
from src import db
bp = Blueprint('web', __name__, url_prefix='/')

query_var = '?'

@bp.route('/')
def index():
    return render_template('wsc/index.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.lite_conn()
        cur = conn.cursor()
        error = None
        select_user = f"SELECT * FROM user WHERE username = {query_var}"
        user = cur.execute(select_user, (username,)).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Could not validate credentials."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('web.home_page'))

        print(error)

    return render_template('wsc/login.html')



@bp.route('/home')
def home_page():
    return render_template('wsc/about.html')