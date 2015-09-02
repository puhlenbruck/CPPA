from flask import render_template, url_for, redirect, g, abort, flash, request, abort
from flask.ext.login import login_required, current_user
from app import app
from forms import CharacterForm
import rethinkdb as r
import json
from config import RDB_HOST, RDB_PORT, CP2020_DB

# open connection before each request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CP2020_DB)
    except RqlDriverError:
        abort(503, "Database connection could not be established.")

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
    user_id = current_user.get_id()
    chars = r.table('characters').get_all(user_id, index = 'user').run(g.rdb_conn)
    print chars
    return render_template('characterindex.html', characters = chars)
    
@app.route('/characters/new', methods = ['GET', 'POST'])
@login_required
def character_create():
    form = CharacterForm()
    if form.validate_on_submit():
        char_id = autoinc_id(r.table('characters'))
        r.table('characters').insert({'id':char_id, 'name':form.name.data, 'user': current_user.get_id()}).run(g.rdb_conn)
        return redirect(url_for('character_index'))
    return render_template('charactercreate.html', form = form, title = 'Create New Character')
    

@app.route('/characters/<char_id>', methods = ['GET'])
@login_required
def character_display(char_id):
    character = r.table('characters').get(int(char_id)).run(g.rdb_conn)
    if current_user.get_id() != character['user']:
        abort(401)
    return render_template('characterview.html', title = character['name'], character = character)

    
def autoinc_id(table):
     id_selection = table.get_field('id').run(g.rdb_conn)
     id_list = list(id_selection)
     new_id = len(id_list)+1
     return new_id
