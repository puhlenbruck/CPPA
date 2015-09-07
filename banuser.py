#Takes a single Username as an argument and deactivates that user if it exists

import sys
from useraccountcontrols import deactivate_user
import rethinkdb as r
from config import RDB_HOST, RDB_PORT, CP2020_DB

username = sys.argv[1]
conn = r.connect(host=RDB_HOST,port=RDB_PORT,db=CP2020_DB)
user = r.table('users').get_all(username, index='username')
if len(list(user.run(conn)))!=1:
    print '**FAIL** User Does not Exist'
    sys.exit()
deactivate_user(user,conn)
print list(user.run(conn))[0]['username'] + ' deactivated'
