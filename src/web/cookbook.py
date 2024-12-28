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

# New Recipe
@bp.route('/new', methods=('GET', 'POST'))
@auth.authorize_login
def new_recipe():
    conn = db.lite_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cookbook_category WHERE user_id = ?;", (session['user_id'],))
    categories = cur.fetchall()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['ckeditor']
        keywords = request.form['keywords'].split(',')
        user_id = session.get('user_id')

        error = None

        conn = db.lite_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO recipe (user_id, title, recipe, keywords) VALUES (?,?,?,?);",
                        (user_id, title, body, request.form['keywords']))
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

        cur.execute("SELECT * FROM cookbook_category WHERE user_id = ?;", (user_id,))
        categories = cur.fetchall()
        print(request.form)
        for category in categories:
            print(category['id'])
            if str(category['id']) in request.form:
                print(category['id'])
                cur.execute("INSERT INTO recipe_category (recipe_id, category_id) VALUES (?,?);",
                            (recipe_id[0], category['id']))
                conn.commit()

        if error:
            flash(error)
        else:
            flash("New recipe logged!")

        return redirect(url_for('web.cookbook'))
    
    return render_template('cookbook/new.html', categories=categories)

# New category
@bp.route('/new_category', methods=['POST'])
@auth.authorize_login
def new_category():
    category = request.form['category']
    conn = db.lite_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cookbook_category (user_id, name) VALUES (?,?);",
                (session['user_id'], category)
                )
    conn.commit()
    return redirect(url_for("web.cookbook"))

'''
Read
'''

@bp.route('/view/<recipe_id>', methods=('GET', 'POST'))
@auth.authorize_login
def recipes(recipe_id):
    conn = db.lite_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipe WHERE id = ?",
                (recipe_id,)
                )
    recipe = cur.fetchone()
    return render_template('cookbook/view.html', recipe=recipe)

'''
Update
'''

@bp.route('/edit/<recipe_id>', methods=('GET', 'POST'))
@auth.authorize_login
def edit_recipe(recipe_id):
    conn = db.lite_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['ckeditor']
        new_keywords = request.form['keywords'].split(',')
        user_id = session.get('user_id')

        error = None
        # RECIPE KEYWORDS UPDATE
        cur.execute("SELECT keyword FROM recipe_keyword WHERE user_id = ? AND recipe_id = ?;",
                    (user_id, recipe_id)
                    )
        keywords = cur.fetchall()
        old_keywords = []
        for keyword in keywords:
            old_keywords.append(keyword[0])
        del_keywords = [item for item in old_keywords if item not in new_keywords]
        add_keywords = [item for item in new_keywords if item not in old_keywords]
        for keyword in del_keywords:
            cur = conn.cursor()
            cur.execute("DELETE FROM recipe_keyword WHERE user_id = ? AND recipe_id = ? AND keyword = ?;",
                        (user_id, recipe_id, keyword)
                        )
            conn.commit()
            cur.close()
        for keyword in add_keywords:
            cur = conn.cursor()
            cur.execute("INSERT INTO recipe_keyword (user_id, recipe_id, keyword) VALUES (?,?,?);",
                        (user_id, recipe_id, keyword)
                        )
            conn.commit()
            cur.close()

        #RECIPE CATEGORIES UPDATED
        cur.execute("SELECT * FROM cookbook_category WHERE user_id = ?;", (user_id,))
        categories = cur.fetchall()
        cur.execute('SELECT * FROM recipe_category WHERE recipe_id = ?;', (recipe_id,))
        recipe_categories = cur.fetchall()
        recipe_cat_list = []
        if recipe_categories is not None:
            for recipe_category in recipe_categories:
                recipe_cat_list.append(recipe_category['category_id'])
        print(recipe_cat_list)

        if categories is not None:
            cat_chage = None
            for category in categories:
                conn = db.lite_conn()
                cur = conn.cursor()
                print(category['id'])
                print(request.form)
                if str(category['id']) in request.form:
                    print(type(category['id']), type(recipe_id), recipe_id)
                if str(category['id']) in request.form and category['id'] not in recipe_cat_list:
                    cur.execute("INSERT INTO recipe_category (recipe_id, category_id) VALUES (?,?);",
                                (int(recipe_id), int(category['id']))
                                )

                elif category['id'] in recipe_cat_list and str(category['id']) not in request.form:
                    print('Delete?')
                    cur.execute('DELETE FROM recipe_category WHERE recipe_id = ? AND category_id = ?;',
                                (int(recipe_id), int(category['id']))
                                )
                conn.commit()
                cur.close()


        # RECIPE UPDATED
        cur = conn.cursor()
        cur.execute("UPDATE recipe SET title = ?, recipe = ?, keywords = ? WHERE user_id = ? AND id = ?;",
                    (title, body, request.form['keywords'], user_id, recipe_id)
                    )
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('web.cookbook.recipes', recipe_id=recipe_id))

    cur.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,))
    recipe = cur.fetchone()
    cur.execute('SELECT * FROM cookbook_category WHERE user_id = ?;', (session['user_id'],))
    categories = cur.fetchall()
    cur.execute("SELECT * FROM recipe_category WHERE recipe_id = ?;",
                (recipe_id,))
    cat_ids = cur.fetchall()
    cat_list = []
    for id in cat_ids:
        cat_list.append(id['category_id'])
    cur.close()
    conn.close()

    return render_template('cookbook/edit.html', recipe=recipe, categories=categories, cat_list=cat_list)

'''
Delete
'''

@bp.route('/delete/<recipe_id>', methods=('GET', 'POST'))
@auth.authorize_login
def delete_recipe(recipe_id):
    if request.method == 'POST':
        conn = db.lite_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM recipe WHERE id = ?;", (recipe_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('web.cookbook'))
