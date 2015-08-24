from flask.ext.login import LoginManager
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash
from config import RDB_HOST, RDB_PORT, CP2020_DB
import rethinkdb as r

login_manager = LoginManager()
login_manager.login_view = "users.login"
salt_size = 128
cpu_cost = 32768
memory_cost = 8

@login_manager.user_loader
def load_user(username):
    conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CP2020_DB)
    user = r.table('users').get_all(username, index = 'username').run(conn)
    
    user = list(user)
    print user
    if len(user) == 1:
        return user[0]
    else:
        return None
    
    
def validate_credentials(username, password):
    print 'validating ',
    user = load_user(username)
    print user
    if user != None:
        print 'user loaded'
        return validate_password(user, password)
    else: 
        salt = generate_random_salt(salt_size)
        generate_password_hash(password, salt, N=cpu_cost, r=memory_cost)
        return False
        
        
def validate_password(user, password):
    return check_password_hash(password,user['password'],user['salt'], N=cpu_cost, r=memory_cost)
       
    
    
def create_user_password_hash(user, password):
    user['salt'] = generate_random_salt(salt_size)
    user['password'] = generate_password_hash(password, user['salt'], N=cpu_cost, r=memory_cost)
    return user
    
