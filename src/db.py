import os
import psycopg2
import click
import sqlite3
from flask import Blueprint, current_app, g

bp = Blueprint('db', __name__, url_prefix='/db')

def init_app(app):
    app.teardown_appcontext(close_db)

'''
SQLITE DB CONNECTION
'''

def lite_conn(query='row'):
    if 'db' not in g:
        g.db = sqlite3.connect(os.path.join(current_app.instance_path, current_app.config['LITE_DB']),
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
'''

def pg_conn(service=current_app.config['PG_DB']):
    '''Optional string arg. Returns connection object'''
    if "db" not in g:        
        g.db = psycopg2.connect(
            host=current_app.config['PG_HOST'],
            port=current_app.config['PG_PORT'],
            database=service,
            user=current_app.config['PG_USER'],
            password=current_app.config['PG_PASSWORD']
        )
    return g.db

def ping_conn(service):
    '''Takes string arg. Returns int'''
    close_db()
    res = -1
    if service != "":
        try:
            conn = pg_conn(service)
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
    # If this request connected to the database, close the connection
    db = g.pop("db", None)
    if db is not None:
        db.close()

'''
CLI COMMANDS
Pre-runtime set up commands
'''

@bp.cli.command('init_db')
def init_db():
    '''No args. No returns'''
    conn = pg_conn()
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute('DROP TABLE IF EXISTS books;')
    cur.execute('CREATE TABLE books (title TEXT);')
    conn.commit()
    cur.close()
    conn.close()
