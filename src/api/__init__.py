from flask import Blueprint, render_template, session
import json
from src import auth, db

bp = Blueprint('api', __name__, url_prefix='/api')

'''
USER CRUD
'''
# Create
@bp.route('/register/<username>/<password>')
@auth.login_required
def register_user(username, password):
    new_user_id = auth.register_user(username, password)
    print(type(new_user_id))
    return new_user_id

# Read
@bp.route('/list_users')
@auth.login_required
def list_users():
    user_list = auth.list_users()
    return user_list

# Update
@bp.route('/update/<username>/<password>/<new_username>')
@auth.login_required
def update_username(username, password, new_username):
    if session['username'] == username:
        updated_name = auth.update_username(username, password, new_username)
    else:
        msg = "Can only change your own username"
        return msg
    if updated_name == -1:
        msg = "Error updating username: Check credentials."
    else:
        msg = f"Your new username is: {updated_name}"
    return msg

@bp.route('/service_login/<service>')
def service_login(service):
    session['service'] = service
    msg = f"Now using {session['service']}"
    return msg

@bp.route('/login/<service>/<username>/<password>')
def login(service, username, password):
    user_info = auth.login_user(service, username, password)
    msg = f"Welcome {session['username']}"
    return msg

@bp.route('/logout')
def logout():
    auth.logout()
    msg = "Session cleared"
    return msg

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