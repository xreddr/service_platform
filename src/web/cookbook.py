import functools
import sqlite3
import werkzeug.exceptions
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, flash, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth
# CKEditor
from flask import Flask
from flask_ckeditor import CKEditor

current_app.config.update(CKEDITOR_SERVE_LOCAL='ON', CKEDITOR_HEIGHT=400)
ckeditor = CKEditor(current_app)


bp = Blueprint('cookbook', __name__, url_prefix='cookbook')


'''
Create
'''


@bp.route('/new', methods=('GET', 'POST'))
@auth.authorize_login
def new_recipe():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['recipe']
        keywords = request.form['keywords'].split(',')
        keywords_string = json.dumps(keywords)
        user_id = session.get('user_id')
        # print(title)
        # print(body)
        # print(type(keywords), type(keywords_string))
        # print(keywords_string)
        # print(user_id)
        error = None

        conn = db.lite_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO recipe (user_id, title, recipe, keywords) VALUES (?,?,?,?);",
                        (user_id, title, body, keywords_string))
        except sqlite3.IntegrityError:
            error = "Recipe already exists!"
        print(error)
        conn.commit()

        recipe_id = cur.execute("SELECT id FROM recipe WHERE user_id = ? AND title = ?;",
                    (user_id, title)).fetchone()
        for keyword in keywords:
            cur.execute("INSERT INTO recipe_keyword (recipe_id, user_id, keyword) VALUES (?,?,?);",
                        (recipe_id[0], user_id, keyword)
                        )
            conn.commit()
            print(keyword)

        if error:
            flash(error)
        else:
            flash("New recipe logged!")

        return redirect(url_for('web.cookbook'))
    
    return render_template('cookbook/new.html')

'''
Read
'''

@bp.route('/recipes', methods=('GET', 'POST'))
@auth.authorize_login
def recipes():
    return redirect(url_for('web.cookbook'))

'''
Update
'''

@bp.route('/edit', methods=('GET', 'POST'))
@auth.authorize_login
def edit_recipe():
    return redirect(url_for('web.cookbook'))

'''
Delete
'''

@bp.route('/delete', methods=('GET', 'POST'))
@auth.authorize_login
def delete_recipe():
    return redirect(url_for('web.cookbook'))
