import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError
from config import RDB_HOST, RDB_PORT, CP2020_DB


TABLE_NAMES = ['test', 'users', 'characters']

# db setup; only run once
def db_setup():
    print 'Setting up database'
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    db_create(connection)
    connection.use(CP2020_DB)
    table_create(connection)
    table_options(connection)
    connection.close()
    print 'Database setup completed'

def table_create(connection):
    for table in TABLE_NAMES:
        try:
            r.table_create(table).run(connection)
            print 'Table ' + table + ' created'
        except RqlRuntimeError:
            print 'Table ' + table + ' already exists'
            
def table_options(connection):
    try:
        r.table('users').index_create('username').run(connection)
        print 'username index added'
    except RqlRuntimeError:
        print 'username index already exists'
    try:
        r.table('characters').index_create('name').run(connection)
        print 'character name index added'
    except RqlRuntimeError:
        print 'character name index already exists'
    try:
        r.table('characters').index_create('user').run(connection)
        print 'character user index added'
    except RqlRuntimeError:
        print 'character user index already exists'
    

def db_create(connection):
    try:
        r.db_create(CP2020_DB).run(connection)
        print 'Database created'
    except RqlRuntimeError:
        print 'Database already exists'


# DANGEROUS
# drop everything and create a new, empty database      
def db_reset():
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
