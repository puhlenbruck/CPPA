from flask import render_template, url_for, redirect, g, abort
from app import app
from forms import TaskForm
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

# rethink config
RDB_HOST = 'localhost'
RDB_PORT = 28015
CP2020_DB = 'cyberpunk'

# db setup; only run once
def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(CP2020_DB).run(connection)
        r.db(CP2020_DB).table_create('test').run(connection)
        print 'Database setup completed'
    except RqlRuntimeError:
        print 'Database already exists.'
    finally:
        connection.close()
dbSetup()

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
	return render_template('index.html', form = form, tasks = selection)
