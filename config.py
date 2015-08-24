import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

# rethink config
RDB_HOST = 'localhost'
RDB_PORT = 28015
CP2020_DB = 'cyberpunk'

# db setup; only run once
def dbSetup():
    print 'Setting up database'
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    dbCreate(connection)
    tablesCreate(connection)
    connection.close()
    print 'Database setup completed'

def tablesCreate(connection):
    try:
        r.db(CP2020_DB).table_create('test').run(connection)
        print 'Table created'
    except RqlRuntimeError:
        print 'Table already exists'

def dbCreate(connection):
    try:
        r.db_create(CP2020_DB).run(connection)
        print 'Database created'
    except RqlRuntimeError:
        print 'Database already exists'


# DANGEROUS
# drop everything and create a new, empty database      
def dbReset():
    if yn_choice("Are you sure you wish to reset the Database?\nAll data will be lost and this cannot be undone.", 'n'):
        connection = r.connect(host=RDB_HOST, port=RDB_PORT, db=CP2020_DB)
        try:
            r.db_drop(CP2020_DB).run(connection)
            print 'Database deleted'
        except RqlRuntimeError:
            print 'Database could not be deleted'
        finally:
            connection.close()
        dbSetup()
    
def yn_choice(message, default='n'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return choice.strip().lower() in values
