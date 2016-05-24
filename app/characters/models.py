from flask import g
import rethinkdb as r
from .character.attributes import default_attributes

class Character(object):
        name=None
        user=None
        id=None
        role=None
        attributes=None
        skills=None

        def __init__(self, db_data):
            self.name = db_data['name']
            self.user = db_data['user']
            self.id = db_data['id']
            self.role = db_data.get('role','Character')
            self.attributes=db_data.get('attributes',default_attributes())
            self.skills=db_data.get('skills')

def load_character(id):
    character=Character(r.table('characters').get(id).run(g.rdb_conn))
    return character
