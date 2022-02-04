import mysql.connector
from decouple import config

db_host = config('DB_HOST')
db_user = config('DB_USER')
db_passwd = config('DB_PASSWD')
db_database_name = config('DB_DATABASE_NAME')

db = mysql.connector.connect(
    host=db_host, user=db_user, passwd=db_passwd, database=db_database_name)
