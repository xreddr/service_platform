from flask import Blueprint, render_template, session, request, jsonify
import json
from src import auth, db

bp = Blueprint('api', __name__, url_prefix='/api')

'''
USER CRUD
Only existing users can create new users
Users can only delete themselves
'''

# CREATE
# Register new user on stated service

@bp.route('/register', methods=['POST'])
@auth.login_required
def register_user():
    '''Takes json object; string values. Returns json object.'''
    req = request.get_json()
    user_info = auth.register_user(req['service'], req['username'], req['password'])
    res = json.dumps(user_info)
    return res

# READ
# Read all users on current session service

@bp.route('/list_users', methods=['GET'])
@auth.login_required
def list_users():
    user_list = auth.list_users()
    return user_list

# UPDATE
# Update logged in user information only

@bp.route('/update/username', methods=['POST'])
@auth.login_required
def update_username():
    req = request.get_json()
    if session['username'] == req['username']:
        updated_name = auth.update_username(req['username'], req['password'], req['new_username'])
    else:
        msg = "Can only change your own username"
        return msg
    if updated_name == -1:
        msg = "Error updating username: Check credentials."
    else:
        msg = f"Your new username is: {updated_name}"
    return msg

@bp.route('/update/password')
@auth.login_required
def update_password():
    req = request.get_json()
    if session['username'] == req['username']:
        updated_password = auth.update_password(req['username'], req['password'], req['new_password'])
    else:
        error = "Not logged into requested user's profile"
        return jsonify(error)
    return jsonify(updated_password)

# DELETE
# Delete logged in users auth info

@bp.route('/delete', methods=['POST'])
@auth.login_required
def delete_user():
    req = request.get_json()
    error = None

    if not session['username'] == req['username']:
        error = "Cannot delete other users"
        return jsonify(error)
    if error is None:
        raw_res = auth.delete_user(req['username'], req['password'])
    return jsonify(raw_res)


'''
LOGIN ROUTES
'''

@bp.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    user_info = auth.login_user(req['service'], req['username'], req['password'])
    res = json.dumps(user_info)
    return res

@bp.route('/logout')
def logout():
    auth.logout()
    msg = "Session cleared"
    return msg

'''
TESTING
Module off anything useful
'''

@bp.route('/test')
@auth.login_required
def test_page():
    return render_template('about.html')

@bp.route('/home')
def home():
    username = 'None'
    service = 'None'
    if session:
        try:
            if session['username']:
                username = session['username']
        except KeyError:
            pass
        try:
            if session['service']:
                service = session['service']
        except KeyError:
            pass

    msg = f"Session User: {username}, Session Service: {service}"

    return msg