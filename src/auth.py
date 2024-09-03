import psycopg2
import functools
from flask import Blueprint, current_app, g, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from .db import pg_conn, ping_conn, lite_conn

bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
RESPONCE FORMAT
All returns from this module use the res dict.
'''

res = {
    "code" : None,
    "body" : None
}
code = {
    "pass" : 0,
    "fail" : -1
}

query_var = '?'

'''
USER AUTH FUNCTIONS
User CRUD functions requiring password authorizing
Session handling
SQLITE CONVERSION
'''

# CREATE

def register_user(username, password):
    '''Takes strings. Returns res dict.'''
    error = None
    conn = lite_conn()

    insert_user = f"INSERT INTO user (username, password) VALUES ({query_var}, {query_var})"
    select_user = f"SELECT id, username FROM user WHERE username = {query_var}"

    cur = conn.cursor()
    try:
        cur.execute(insert_user, (username, generate_password_hash(password)))
    except (psycopg2.errors.UniqueViolation):
        error = "User already exists"
    conn.commit()

    if error is None:
        cur.execute(select_user, (username,))
        user_info = cur.fetchone()

    cur.close()
    conn.close()

    if user_info:

        res.update({
            "code": code['pass'], 
            "body" : {
                "user_id":user_info[0],
                "username":user_info[1]
            }
        })
        
    else:
        res.update({"code": code['fail'], "body": error})

    return res

# READ

def list_users():
    '''Takes none. Returns res dict.'''
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()

    cur.execute(
        "SELECT id, user_name FROM user_auth"
    )
    user_list = cur.fetchall()
    res.update({
        "code": code['pass'],
        "body": user_list
    })

    return res

# UPDATE
# Functions can be combined

def update_username(username, password, new_username):
    '''Takes string args. Returns res dict'''
    error = None

    # User creds query
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM user_auth WHERE user_name = %s;",
        (username,)
    )
    user_info = cur.fetchone()
    user_id = user_info[0]
    pass_check = user_info[2]

    # Password validation
    if not check_password_hash(pass_check, password):
        error = "Incorrect credentials"

    if error is None:
        # Update and validation queries
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
        res.update({"code": code['pass'], "body": user_name})
    else:
        res.update({"code": code['fail'], "body": error})
    
    return res

def update_password(username, password, new_password):
    '''Takes string args. Returns res dict.'''
    error = None

    # User creds query
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM user_auth WHERE user_name = %s;",
        (username,)
    )
    user_info = cur.fetchone()
    user_id = user_info[0]
    pass_check = user_info[2]

    # Password validation
    if not check_password_hash(pass_check, password):
        error = "Incorrect credentials"

    if error is None:
        # Update and validation queries
        cur.execute(
            "UPDATE user_auth SET password = %s WHERE id = %s;",
            (generate_password_hash(new_password), user_id)
        )
        conn.commit()
        cur.execute(
            "SELECT password FROM user_auth WHERE id = %s;",
            (user_id,)
        )
        pass_tmp = cur.fetchone()
        pass_check = pass_tmp[0]
        if not check_password_hash(pass_check, new_password):
            error = "New password could not be validated"
            res.update({"code": code['fail'], "body": error})
        else:
            msg = "Password updated"
            res.update({"code": code['pass'], "body": msg})
    else:
        res.update({"code": code['fail'], "body": error})
    
    return res

# DELETE

def delete_user(username, password):
    '''Takes string args. Returns res dict.'''
    error = None
    conn = pg_conn(service=session['service'])
    cur = conn.cursor()

    # User info validation query
    cur.execute(
        "SELECT * FROM user_auth WHERE user_name = %s;",
        (username,)
    )
    auth_info = cur.fetchone()
    user_id = auth_info[0]
    pass_check = auth_info[2]
    if not check_password_hash(pass_check, password):
        error = "Incorrect credentials."

    if error is None:
        # Delete query
        cur.execute(
            "DELETE FROM user_auth WHERE id = %s;",
            (user_id,)
        )
        conn.commit()
        msg = "User deleted"
        res.update({"code": code['pass'], "body": msg})
    else:
        res.update({"code": code['fail'], "body": error})

    cur.close()
    conn.close()
    return res

'''
LOGIN FUNCTIONS
'''

def login_user(username, password):
    '''Takes strings. Returns res dict.'''
    conn = lite_conn()
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
        res.update({ 
            "code" : code['pass'], 
            "body" : {
                "user_id" : user['id'],
                "username" : user['username']
                }
        })
    else:
        res.update({ "code" : code['fail'], "body" : error})
    
    return res

def logout():
    '''Takes none. Gives none.'''
    session.clear()

'''
API WRAPPERS
Set auth levels for routes
'''

@bp.before_app_request
def load_logged_in_user():
    '''Takes none. Gives none.'''
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        cur = lite_conn().cursor()
        cur.execute(f"SELECT * FROM user WHERE id = {query_var};", (user_id,))
        g.user = cur.fetchone()
    

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        '''Takes view. Returns view or res dict.'''
        if g.user is None:
            error = "Login is required"
            res.update({
                "code": code['fail'],
                "body" : error
            })
            return res
        
        return view(**kwargs)
    
    return wrapped_view


'''
WEB WRAPPERS
'''

def open_reg_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        '''Takes view. Returns view.'''
        try:
            if current_app.config['OPEN_REG'] != True and g.user['role'] != current_app.config['ADMIN_CODE']:
                return redirect(url_for('web.index'))
        except IndexError:
            return redirect(url_for('web.index'))

        return view(**kwargs)
    
    return wrapped_view
        
def authorize_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('web.index'))
        return view(**kwargs)
    return wrapped_view
