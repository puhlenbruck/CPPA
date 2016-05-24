from flask import g
import rethinkdb as r
import random
from .character.attributes import default_attributes, ATTRIBUTES

class Character(object):
        skills=0;

        def __init__(self, db_data):
            self.name = db_data['name']
            self.user = db_data['user']
            self.id = db_data['id']
            self.role = db_data.get('role','Character')
            self.attributes=db_data.get('attributes',default_attributes())
            for attr in ATTRIBUTES:
                key = attr.get('abbr')
                if not self.attributes.get(key):
                    self.attributes[key]={'value':0, 'skills':[]}
                if not self.attributes.get(key).get('skills'):
                    self.attributes[key]['skills'] = []
                for skill in attr.get('skills'):
                    if skill not in map(lambda char_skill: char_skill['name'], self.attributes.get(key).get('skills')):
                        self.attributes[key]['skills'].append({'name':skill,'value':0})
                self.attributes[key]['skills'].sort(key=lambda s: s.get('name'))
                self.skills += len(self.attributes[key]['skills'])
            self.attributes = list(self.attributes.items())
            self.attributes.sort(key=lambda a: a[0])

def load_character(id):
    character=Character(r.table('characters').get(id).run(g.rdb_conn))
    return character

def create_new_character(char_data):
    char_data['id'] = rand_id()
    r.table('characters').insert(char_data).run(g.rdb_conn)
    return char_data


def rand_id():
    while True:
        id = random.getrandbits(24)
        if r.table('characters').get(id).run(g.rdb_conn) is None:
            return id;
