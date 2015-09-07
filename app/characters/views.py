from flask import render_template, url_for, redirect, g, abort, flash, request, abort
from flask.ext.login import login_required, current_user
from app import app
from forms import CharacterForm
from dbcontrols import autoinc_id
import rethinkdb as r
import json
from config import RDB_HOST, RDB_PORT, CP2020_DB
from wtforms.fields import TextField, IntegerField
from wtforms.validators import Required

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
    return render_template('characters/characterindex.html', characters = chars)
    
@app.route('/characters/new', methods = ['GET', 'POST'])
@login_required
def character_create():
    form = CharacterForm()
    if form.validate_on_submit():
        char_id = autoinc_id(r.table('characters'), g.rdb_conn)
        r.table('characters').insert({'id':char_id, 'name':form.name.data, 'user': current_user.get_id()}).run(g.rdb_conn)
        return redirect(url_for('character_index'))
    return render_template('characters/charactercreate.html', form = form, title = 'Create New Character')
    

@app.route('/characters/<char_id>', methods = ['GET'])
@login_required
def character_display(char_id):
    character = r.table('characters').get(int(char_id)).run(g.rdb_conn)
    if current_user.get_id() != character['user']:
        abort(401)
    return render_template('characters/characterview.html', title = character['name'], character = character)

@app.route('/characters/<char_id>/edit', methods = ['GET','POST'])
@login_required
def character_edit(char_id):
    character = r.table('characters').get(int(char_id)).run(g.rdb_conn)
    if current_user.get_id() != character['user']:
        abort(401)
    form = CharacterForm()
    if form.validate_on_submit():
        char_attributes = {'INT':form.intelligence.data, 'REF':form.reflex.data, 'TECH':form.tech.data, 'COOL':form.cool.data, 'ATTR':form.attractivness.data, 'LUCK':form.luck.data, 'MA':form.movement_allowance.data, 'EMP':form.empathy.data}
        for key in char_attributes:
            if char_attributes[key] is None:
                char_attributes[key] = 0
        r.table('characters').get(int(character['id'])).update({'name':form.name.data, 'role':form.role.data.lower(), 'attributes':char_attributes}).run(g.rdb_conn)
        return redirect(url_for('character_display', char_id=character['id']))
   
    form.name.data = character.get('name')
    form.role.data = character.get('role')
    char_attributes = character.get('attributes')
    if char_attributes:
        form.intelligence.data = char_attributes.get('INT')
        form.reflex.data = char_attributes.get('REF')
        form.tech.data = char_attributes.get('TECH')
        form.cool.data = char_attributes.get('COOL')
        form.attractivness.data = char_attributes.get('ATTR')
        form.luck.data = char_attributes.get('LUCK')
        form.movement_allowance.data = char_attributes.get('MA')
        form.empathy.data = char_attributes.get('EMP')
    
    return render_template('characters/characteredit.html', form = form, title = 'edit: ' + character['name'], character = character)
