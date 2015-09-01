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
    user_char_ids = current_user.get_data()['characters']
    chars = []
    for char_id in user_char_ids:
        character = r.table('characters').get('id').run(g.rdb_conn)
        chars.append(character)
    return render_template('characterindex.html', characters = chars)
    
@app.route('/characters/new', methods = ['GET'])
@login_required
def character_create():
    return render_template('characterindex.html')
