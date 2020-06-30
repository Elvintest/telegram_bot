import mysql.connector

dbconfig = {'host': '95.181.198.40',
            'user': 'root',
            'password': 'scartown89',
            'database': 'TEST'}
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