from flask import render_template, url_for, redirect, g, abort
from app import app
import rethinkdb as r
from config import RDB_HOST, RDB_PORT, CP2020_DB
from forms import LoginForm
from app.auth import validate_credentials

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
        
        
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if validate_credentials(form.username.data, form.password.data):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', title = 'Cyberpunk2020', form = form, error='invalid username or password')
    return render_template('login.html', title = 'Cyberpunk2020', form = form)
