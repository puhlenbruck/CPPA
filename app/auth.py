from flask.ext.login import LoginManager
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash
from config import RDB_HOST, RDB_PORT, CP2020_DB
from app.users.models import load_username, User
import rethinkdb as r

login_manager = LoginManager()
login_manager.login_view = "login"
salt_size = 128
hash_size = 128
cpu_cost = 32768
memory_cost = 8


@login_manager.user_loader
def load_user(user_id):
    conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CP2020_DB)
    user = r.table('users').get(user_id).run(conn)
    conn.close()
    return User(user)
  
    
def validate_credentials(username, password):
    user = load_username(username)
    if user != None:
        if validate_password(user, password):
            return user
        else: 
            return None
    else: 
        salt = generate_random_salt(salt_size)
        generate_password_hash(password, salt, N=cpu_cost, r=memory_cost)
        return None
        
        
def validate_password(user, password):
    return check_password_hash(password,user['password'],user['salt'], N=cpu_cost, r=memory_cost, buflen = hash_size)
       
    
    
def create_password_hash(password):
    pwdhash = {'salt':None, 'password':None}
    pwdhash['salt'] = generate_random_salt(salt_size)
    pwdhash['password'] = generate_password_hash(password, pwdhash['salt'], N=cpu_cost, r=memory_cost, buflen=hash_size)
    return pwdhash
    
