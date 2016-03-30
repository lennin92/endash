
DB_HOST = ''
DB_PORT = ''
DB_USER = ''
DB_PASS = ''
DB_NAME = ''

import MySQLdb

db=MySQLdb.connect(host = DB_HOST,
                   port = DB_PORT,
                   user = DB_USER,
                   passwd=DB_PASS,
                   db=DB_NAME)


