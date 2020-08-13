import mysql.connector
import os,sys
from dotenv import load_dotenv
home = os.getcwd()
dotenv_path = os.path.join(home, 'variables.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print('variables wasnt found')

dbconfig = {'host': os.environ['DB_USER'],
            'user': os.environ['USER'],
            'password': os.environ['PASSWORD_DB'],
            'database': os.environ['DATA_BASE_NAME']}
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()
_show_tables = """show tables"""
create_user_notices = """CREATE TABLE user_notices (
  user_id int(11) NOT NULL,
  date date DEFAULT NULL,
  body text NOT NULL
);"""
create_user_states = """CREATE TABLE user_states (
  process_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  state varchar(40) NOT NULL,
  PRIMARY KEY (process_id),
  UNIQUE KEY user_id (user_id)
);"""
cursor.execute(create_user_notices)
cursor.execute(create_user_states)
conn.commit()
cursor.execute(_show_tables)
tables = cursor.fetchall()
print(tables)