from flask import Blueprint, render_template, session, request, jsonify, g, current_app
from src import auth, db

bp = Blueprint('api', __name__, url_prefix='/api')

'''
RESPONSE FORMAT
'''

from flask_cors import CORS
cors = CORS(current_app, resources={r"/api/*": {"origins": "*"}})
current_app.config['CORS_HEADERS'] = 'Content-Type'

def res(body):
    response = jsonify(body)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


'''
USER CRUD
Self registration
Users can only delete themselves
'''


# CREATE
# Register new user on stated service

@bp.route('/register', methods=['POST'])
def register_user():
    '''Takes json object; string values. Returns json object.'''
    req = request.get_json()
    user_info = auth.register_user(req['service'], req['username'], req['password'])
    response = res(user_info)
    return response

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
    response = res(msg)
    return response

@bp.route('/update/password')
@auth.login_required
def update_password():
    req = request.get_json()
    if session['username'] == req['username']:
        updated_password = auth.update_password(req['username'], req['password'], req['new_password'])
    else:
        error = "Not logged into requested user's profile"
        return jsonify(error)
    response = res(updated_password)
    return response

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
    response = res(raw_res)
    return response


'''
LOGIN ROUTES
'''


@bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user_info = auth.login_user(body['service'], body['username'], body['password'])
    response = res(user_info)
    return response

@bp.route('/logout')
def logout():
    auth.logout()
    response = res("Session Cleared")
    return response


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
    body = {}
    if session.get('service'):
        for i in session:
            body.update({i: session[i]})
    body.update({
        "endpoints" : {
            "register" : "Make an account with json values 'service', 'username', 'password'",
            "login" : "Login with json values 'service', 'username', 'password'",
            "logout" : "Deletes session cookie",
            "update/username" : "Takes json values for 'username', 'password', 'new_username'",
            "update/password" : "Takes json values for 'username', 'password', 'new_password'",
            "delete" : "Deletes user with json values 'username', 'password'"
        }
    })
    response = res(body)
    return response

'''
SERVICES
'''

# @bp.route('/start_service', methods=['POST'])
# @auth.login_required
# def service_start():
#     error = None
#     req = request.get_json()
#     if not req['owner'] == session.get('username'):
#         error = "You can only create a service for yourself"
#     else:
#         service_res = services.start_service(req['svc_name'], session.get('user_id'), req['password'])
    
#     if error is None:
#         res.update({
#             "code": service_res['code'],
#             "body": service_res
#         })
#     else:
#         res.update({
#             "code": auth.code['fail'],
#             "body": error
#         })

#     return jsonify(res)
    