import os
import psycopg2
import click
from flask import Blueprint, current_app, g

bp = Blueprint('db', __name__, url_prefix='/db')

def init_app(app):
    app.teardown_appcontext(close_db)

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
    res = -1
    if service != "":
        try:
            conn = pg_conn(service)
            print("CONNECTED")
            conn.close()
            res = 0
        except Exception as er:
            print(f"ERROR:{er}")
            print("NOT CONNECTED TO DB")
            res = -1

    return res

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
