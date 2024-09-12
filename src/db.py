import os
import psycopg2
import click
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Blueprint, current_app, g

bp = Blueprint('db', __name__, url_prefix='/db')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
    app.cli.add_command(init_cookbookdb)


'''
SQLITE DB CONNECTION
'''

def lite_conn(query='row', source=current_app.config['LITE_DB']):
    '''Takes string. Returns session.connection object'''
    if 'db' not in g:
        g.db = sqlite3.connect(os.path.join(current_app.instance_path, source),
                               detect_types=sqlite3.PARSE_DECLTYPES)
        
        if query == 'dict':
            g.db.row_factory = make_dicts
        elif query == 'row':
            g.db.row_factory = sqlite3.Row

    return g.db

def make_dicts(cursor, row):
    '''Takes row object. Returns python dict'''
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


'''
POSTGRES DB CONNECTIONS
!!! CURRENTLY UNUSED
!!! NEEDS ADAPTATION AND TESTING
'''

def pg_conn():
    '''Optional string arg. Returns connection object'''
    if "db" not in g:        
        g.db = psycopg2.connect(
            host=current_app.config['PG_HOST'],
            port=current_app.config['PG_PORT'],
            database=current_app.config['PG_DB'],
            user=current_app.config['PG_USER'],
            password=current_app.config['PG_PASSWORD']
        )
    return g.db

def ping_conn():
    '''Takes string arg. Returns int'''
    close_db()
    res = -1
    try:
        conn = pg_conn()
        print("CONNECTED")
        if conn == g.db:
            res = 0
    except Exception as er:
        print(f"ERROR:{er}")
        print("NOT CONNECTED TO DB")
        res = -1
    close_db()
    return res


'''
CLOSE CURRENT DB
'''


def close_db(e=None):
    '''Optional arguement. No return'''
    # If this request connected to the database, close the connection
    db = g.pop("db", None)
    if db is not None:
        db.close()



'''
CLI COMMANDS
Pre-runtime set up commands
'''

# Run First
@bp.cli.command('init-db')
def init_db():
    '''No args. No returns'''
    db = lite_conn()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    cur = db.cursor()

    cur.execute("INSERT INTO user (username, password, role) VALUES (?,?,?);",
                (current_app.config['DEFAULT_USER'], generate_password_hash(current_app.config['DEFAULT_PASSWORD']), current_app.config['ADMIN_CODE'])
                )

    db.commit()
    cur.close()
    db.close()

@bp.cli.command('init-cookbookdb')
def init_cookbookdb():
    '''No args. No returns'''
    # Writes the cookbook database
    db = lite_conn()
    with current_app.open_resource('cookbook.sql') as f:
        db.executescript(f.read().decode('utf8'))
    cur = db.cursor()

    cur.execute("INSERT INTO recipe (title, recipe) VALUES (?,?);",
                ('Sampe', 'A bit of this, a bit of that')
                )
    try:
        cur.execute("INSERT INTO service (name, link) VALUES (?,?);",
                    ('cookbook', 'cookbook.sqlite')
        )
    except sqlite3.IntegrityError:
        pass
        
    db.commit()
    cur.close()
    close_db()
