from flask import render_template, g, abort
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

@app.route('/', methods = ['GET', 'POST'])
def index():
	return render_template('index.html')
