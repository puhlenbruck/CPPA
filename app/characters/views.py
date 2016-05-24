from flask import render_template, url_for, redirect, g, abort, flash, request, abort
from flask.ext.login import login_required, current_user
from app import app
from .forms import CharacterForm
import rethinkdb as r
import random
import base64
from config import RDB_HOST, RDB_PORT, CP2020_DB
from wtforms.fields import TextField, IntegerField
from wtforms.validators import Required
from .character.attributes import ATTRIBUTES
from .models import load_character

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

@app.route('/characters', methods = ['GET'])
@login_required
def character_index():
    user_id = current_user.get_id()
    db_chars = r.table('characters').get_all(user_id, index = 'user').run(g.rdb_conn)
    web_chars = []
    for c in db_chars:
        c['id'] = int_to_b64_string(c.get('id'))
        web_chars.append(c)
    return render_template('characters/characterindex.html', characters = web_chars)

@app.route('/characters/new', methods = ['GET', 'POST'])
@login_required
def character_create():
    form = CharacterForm()
    if form.validate_on_submit():
        char_id = rand_id()
        r.table('characters').insert({'id':char_id, 'name':form.name.data, 'user': current_user.get_id()}).run(g.rdb_conn)
        return redirect(url_for('character_index'))
    return render_template('characters/charactercreate.html', form = form, title = 'Create New Character')

def rand_id():
    while True:
        id = random.getrandbits(24)
        if r.table('characters').get(id).run(g.rdb_conn) is None:
            return id;


@app.route('/characters/<char_id>', methods = ['GET'])
@login_required
def character_display(char_id):
    character = load_character(b64_str_to_int(char_id))
    if character is None or current_user.get_id() != character.user:
        abort(404)
    character.id = char_id
    return render_template('characters/characterview.html', title = character.name, character = character, attributes=ATTRIBUTES)

@app.route('/characters/<char_id>/edit', methods = ['GET','POST'])
@login_required
def character_edit(char_id):
    form = CharacterForm()
    character = r.table('characters').get(b64_str_to_int(char_id)).run(g.rdb_conn)
    if current_user.get_id() != character['user']:
        abort(404)
    if form.validate_on_submit():
        char_attributes = {'INT':form.intelligence.data, 'REF':form.reflex.data, 'TECH':form.tech.data, 'COOL':form.cool.data, 'ATTR':form.attractivness.data, 'LUCK':form.luck.data, 'MA':form.movement_allowance.data, 'EMP':form.empathy.data}
        for key in char_attributes:
            if char_attributes.get(key,None) is None:
                char_attributes[key] = 0
        r.table('characters').get(int(character['id'])).update({'name':form.name.data, 'role':form.role.data.lower(), 'attributes':char_attributes}).run(g.rdb_conn)
        return redirect(url_for('character_display', char_id=char_id))

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
    character['id'] = char_id
    return render_template('characters/characteredit.html', title = 'Edit: ' + character['name'], character = character, form=form)

def int_to_b64_string(int_val):
    return base64.urlsafe_b64encode(int_val.to_bytes(3,'big')).decode('utf-8')

def b64_str_to_int(b64str):
    return int.from_bytes(base64.urlsafe_b64decode(b64str.encode('utf-8')),'big')
