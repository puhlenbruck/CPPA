import rethinkdb as r

def deactivate_user(user, connection):
    user.update({'active':False}).run(connection)   
    
 
def activate_user(user, connection):
    user.update({'active':True}).run(connection)
