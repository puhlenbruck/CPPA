from flask import render_template, url_for, redirect, g, abort, flash
from app import app
import rethinkdb as r
from config import RDB_HOST, RDB_PORT, CP2020_DB
from forms import LoginForm, RegisterForm
from app.auth import validate_credentials, create_user_password_hash

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
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', title = 'Cyberpunk2020', form = form, error='invalid username or password')
    return render_template('login.html', title = 'Cyberpunk2020', form = form)
    
  
@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if not confirm_unique_username(form.username.data):
            error = 'username already exists'
            return render_template('signup.html', title = 'Cyberpunk2020', form = form, error = error)
        if not form.password.data == form.password_confirm.data:
            error = 'passwords do not match'
            return render_template('signup.html', title = 'Cyberpunk2020', form = form, error = error)
        create_user(form.username.data, form.password.data)
        flash('user ' + form.username.data + ' created')
        return redirect(url_for('index'))
    return render_template('signup.html', title = 'Cyberpunk2020', form = form)
    
def create_user(username, password):
    user = {'username': username}
    user = create_user_password_hash(user, password)
    r.table('users').insert(user).run(g.rdb_conn)
    

def confirm_unique_username(username):
    existing_user = r.table('users').get_all(username,index='username').run(g.rdb_conn)
    existing_user = list(existing_user)
    if len(existing_user) != 0:
        return False
    return True
    
