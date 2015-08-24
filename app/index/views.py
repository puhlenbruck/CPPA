from flask import render_template, url_for, redirect, g, abort, Markup, Blueprint, flash, jsonify, request
from app import app
from forms import TaskForm
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

@app.route('/', methods = ['GET', 'POST'])
def index():
	form = TaskForm()
	if form.validate_on_submit():
		r.table('test').insert({"name":form.label.data}).run(g.rdb_conn)
		return redirect(url_for('index'))
	selection = list(r.table('test').run(g.rdb_conn))
	return render_template('index.html', title = 'Cyberpunk2020', form = form, tasks = selection)


_LINK = Markup('<a href="{url}">{name}</a>')
