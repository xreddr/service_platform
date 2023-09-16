import os
import psycopg2
import click
from flask import Blueprint, current_app, session

bp = Blueprint('db', __name__, url_prefix='/db')

'''
POSTGRES DB CONNECTIONS
'''

def pg_conn(service=current_app.config['PG_DB']):
    '''No args. Returns connection object'''
    conn = psycopg2.connect(
        host=current_app.config['PG_HOST'],
        port=current_app.config['PG_PORT'],
        database=service,
        user=current_app.config['PG_USER'],
        password=current_app.config['PG_PASSWORD']
    )
    return conn

def ping_conn(service):
    '''No args. No returns'''
    res = -1
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


# @bp.cli.command('close_db')
def close_db():
    conn = pg_conn()
    cur = conn.cursor()
    cur.close()
    conn.close()
    print('DB CLOSED')

def rollback_db():
    conn = pg_conn()
    conn.rollback()
    conn.close()
    print('Rollback performed')