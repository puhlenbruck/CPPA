from flask import render_template, url_for, redirect, g, abort, flash, request, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
import rethinkdb as r
from config import RDB_HOST, RDB_PORT, CP2020_DB
from .forms import LoginForm, RegisterForm
from app.auth import validate_credentials, create_password_hash
from app.users.models import confirm_unique_username, create_new_user

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
        if current_user.is_authenticated:
            logout_user()
        user = validate_credentials(form.username.data, form.password.data)
        if user is not None:
            
            login_user(user)
            flash('You were logged in')
            next = request.args.get('next')
            if not next_is_valid(next):
                return abort(400)
            return redirect(next or url_for('index'))
        else:
            return render_template('login.html', title = 'Cyberpunk2020', form = form, error='invalid username or password')
    return render_template('login.html', title = 'Cyberpunk2020', form = form)


def next_is_valid(next):
    return True
    

@app.route('/logout/', methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))

  
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
        pwdhash = create_password_hash(form.password.data)
        create_new_user(form.username.data, pwdhash['password'], pwdhash['salt'])
        flash('user ' + form.username.data + ' created')
        return redirect(url_for('index'))
    return render_template('signup.html', title = 'Cyberpunk2020', form = form)
    


    
