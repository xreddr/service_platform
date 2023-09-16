import os
import psycopg2
import json
import functools
from flask import Blueprint, current_app, g, session
from werkzeug.security import check_password_hash, generate_password_hash
from .db import pg_conn, rollback_db, ping_conn

bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
USER AUTH FUNCTIONS
User CRUD functions requiring password authorizing
'''
# Create
def register_user(username, password):
    '''Takes string arguements. Returns string number.'''
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO user_auth (user_name, password) VALUES (%s,%s);",
            (username, generate_password_hash(password))
        )
    except (psycopg2.errors.UniqueViolation):
        print("User already exists")

    conn.commit()
    cur.execute(
        "SELECT id FROM user_auth WHERE user_name = %s;",
        (username,)
    )
    user_id = cur.fetchone()
    user_id = str(user_id[0])

    cur.close()
    conn.close()

    return user_id

# Read
def list_users():
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()

    cur.execute(
        "SELECT id, user_name FROM user_auth"
    )
    user_list = json.dumps(cur.fetchall())

    return user_list

# Update
def update_username(username, password, new_username):
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM user_auth WHERE user_name = %s;",
        (username,)
    )
    user_info = cur.fetchone()
    user_id = user_info[0]
    old_name = user_info[1]
    old_password = user_info[2]
    print(user_id)
    print(type(user_id))
    if check_password_hash(old_password, password):
        cur.execute(
            "UPDATE user_auth SET user_name = %s WHERE id = %s;",
            (new_username, user_id)
        )
        conn.commit()
        cur.execute(
            "SELECT user_name FROM user_auth WHERE id = %s;",
            (user_id,)
        )
        user_name = cur.fetchone()
        user_name = user_name[0]
        session['username'] = user_name
        return user_name
    else:
        return -1

def login_user(service, username, password):
    '''Takes strings. Returns touple.'''
    error = None

    ping = ping_conn(service)
    if ping == 0:
        session['service'] = service
    elif ping == -1:
        error = "Service could not be reached. Check credentials."
        
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()

    if g.user:
        error = "Logout to login to different account"

    cur.execute(
        "SELECT * FROM user_auth WHERE user_name = %s",
        (username,)
    )
    user = cur.fetchone()
    cur.close()

    if user is None:
        error = "Incorrect credentials"
    elif not check_password_hash(user[2], password):
        error = "Credentials incorrect"

    if error is None:
        session.clear()
        session['service'] = service
        session['username'] = user[1]
    else:
        print(error)
    conn.close()
    return user

def logout():
    session.clear()

'''
API WRAPPERS
Set auth levels for routes
'''

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    service = session.get('service')
    if service is None:
        service = current_app.config['PG_DB']
    if username is None:
        g.user = None
    else:
        cur = pg_conn(service).cursor()
        cur.execute("SELECT * FROM user_auth WHERE user_name = %s;", (username,))
        g.user = cur.fetchone()
    

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            msg = "Login required"
            return msg
        
        return view(**kwargs)
    
    return wrapped_view


'''
WEB WRAPPERS
'''