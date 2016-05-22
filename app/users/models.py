from flask import g
from app import app
import rethinkdb as r

class User(object):
    data = []

    def __init__(self, db_data):
        self.data = db_data

    def __getitem__(self, key):
            return self.data[key]

    def get_data(self):
        return self.data

    def is_active(self):
        return self.data['active']

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.data['id']

def load_username(username):
    user = r.table('users').get_all(username, index = 'username').run(g.rdb_conn)
    user = list(user)
    if len(user) == 1:
        return User(user[0])
    else:
        return None

def create_new_user(username, password_hash,salt):
    if not confirm_unique_username:
        return None
    user = {'username':username, 'password':password_hash, 'salt':salt, 'active':True}
    r.table('users').insert(user).run(g.rdb_conn)
    return load_username(user['username'])


def confirm_unique_username(username):
    existing_user = r.table('users').get_all(username,index='username').run(g.rdb_conn)
    existing_user = list(existing_user)
    if len(existing_user) != 0:
        return False
    return True
