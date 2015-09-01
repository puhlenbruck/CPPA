from flask import render_template, url_for, redirect, g, abort, flash, request, abort
from flask.ext.login import login_required, current_user
from app import app
import rethinkdb as r
from config import RDB_HOST, RDB_PORT, CP2020_DB

# open connection before each request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CP2020_DB)
    except RqlDriverError:
        abort(503, "Database connection could be established.")

# close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass
        
@app.route('/characters/', methods = ['GET'])
@login_required
def character_index():
    return render_template('characterindex.html')
    
@app.route('/characters/new', methods = ['GET'])
@login_required
def character_create():
    return render_template('characterindex.html')
