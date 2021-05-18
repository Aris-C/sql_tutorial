'''
****************************************************************************
*  Program  lessson_7.py                                                   *
*  Author   Glenn                                                          *
*  Date     March 27, 2021                                                 *
*  Source   Realpython https://realpython.com/python-sql-libraries/#sqlite *
*  Description:                                                            *
*  This program is used to introduce Geniuses to using a                   *
*  database Structured Query Language (SQL) Join commands.  The program    *
*  imports the sqlite3 module which allows you to create                   *
*  and interact with an SQL Database                                       *
*                                                                          *
*  - The create_connection function is passed the                          *
*    path of the SQLite database file then it connects                     *
*    the app to an exixting SQLite3 database named hgp_pods                *
*    or if it;s not present it creates the database file                   *
*                                                                          *
*  - The execute_query function is passed the path and the                 *
*    query to implement; create_staff_member_table query and               *
*    add_staff_member query                                                *
*                                                                          *
*  - The execute_read function is passed the path and                      *
*    the display_staff_member query                                        *
****************************************************************************
'''

import sqlite3
from sqlite3 import Error

############### Function Definitions *******************

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
#        print("Connection to SQLite DB successful\n")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query,text):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
#        print(f"{text} query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_join_member_leader():
  return """
  SELECT member.name,member.cell,leader.name 
  from member left join leader 
    where leader_id = leader.id order by leader.name
  """

def execute_join_leader_staff():
  return """
  SELECT leader.name,leader.cell,leader.position,staff.name 
  from leader left join staff 
    where staff_id = staff.id order by leader.name
  """

###################  Connect/Create to the Sqlite3 Database File *********************

connection = create_connection("oak8_pods.sqlite7")

##########################  Create staff table variable query ################

create_staff_members_table_query = """
CREATE TABLE IF NOT EXISTS staff (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  cell TEXT NOT NULL,
  position TEXT NOT NULL
);
"""
##########################  Create Pod Leader table variable query ################

create_pod_leaders_table_query = """
CREATE TABLE IF NOT EXISTS leader (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  cell TEXT NOT NULL,
  position TEXT NOT NULL,
  staff_id INTEGER NOT NULL,
  FOREIGN KEY (staff_id) REFERENCES staff (id) 
);
"""

##########################  Create Pod Members table variable query ################

create_pod_members_table_query = """
CREATE TABLE IF NOT EXISTS member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  cell TEXT NOT NULL,
  position TEXT NOT NULL,
  leader_id INTEGER NOT NULL,
  FOREIGN KEY (leader_id) REFERENCES leader (id)
);
"""

#################### Executive queries to create tables #################

execute_query(connection, create_staff_members_table_query,'Create staff') 
execute_query(connection, create_pod_members_table_query,'Create pod members') 
execute_query(connection, create_pod_leaders_table_query,'Create pod leaders') 
print('\n')

################# Create insert queries to add staff, pod members and pod leaders to tables #######
add_staff_members_query = """
INSERT INTO
  staff (name,cell,position)
VALUES
  ('Baba Lemon',       '510.205.0980', 'Senior Innovation Educator'),
  ('Brandon Nicholson','111.111.1111', 'Executive Director'),
  ('Hodari Toure',     '510.435.2594', 'Curriculum Lead'),
  ('Akeeem Brown',     '415.684.0505', 'Programs Director'),
  ('Aaron Hobson',     '510.555.1234', 'Senior Innovation Educator');
"""

add_pod_leaders_query = """
INSERT INTO
  leader (name,cell,position,staff_id)
VALUES
  ('Andrew Lubega',  '925.727.4611','leader',1),
  ('Jacore Baptiste','845.200.6250','leader',2),
  ('Aris Carter',    '510.229.6359','leader',3),
  ('Gabriel Reader', '510.326.5834','leader',4),
  ('Richard Kamau',  '510.228.5623','leader',5);
"""

add_pod_members_query = """
INSERT INTO
  member (name,cell,position,leader_id)
VALUES
  ('Malick',  '510.409.8755', 'member',1),
  ('Ronnin Young',  '415.910.3415', 'member',1),
  ('Glenn Ivory',   '510.328.8290', 'member',1),
  ('Morris',  '925.286.5922', 'member',2),
  ('Prince',  '510.472.0804', 'member',2),
  ('Mousa',   '415.717.8414', 'member',2),
  ('Hyab',    '510.612.3737', 'member',3),
  ('Maurice Richardson', '510.424.7789', 'member',3),
  ('Milan',   '510.816.3232', 'member',3),
  ('Emmanuel','510.934.4133', 'member',4),
  ('Akari Johnson',   '510.500.2206', 'member',4),
  ('David Brickley',   '510.631.6288', 'member',4),
  ('Josaih',  '510.860.5112', 'member',5),
  ('Matthew Dudley', '510.816.2411', 'member',5),
  ('Kymari',  '510.816.2411', 'member',5);
"""

####################  Execute add staff, pod members and pod leaders queries  ##################

execute_query(connection, add_staff_members_query,'Add staff members')
execute_query(connection, add_pod_members_query,'Add pod members')
execute_query(connection, add_pod_leaders_query,'Add pod leaders')
print('\n')



########################### Display staff, members and leader queries ##################### 
display_staff_query = "SELECT * from staff order by name"
staff = execute_read_query(connection, display_staff_query)
print('Staff'.center(13), 'Cell'.center(22), 'Position'.center(24),'\n__________________'.ljust(13),'____________'.ljust(12),'____________________________'.ljust(18))
for staff_member in staff:
  print(staff_member[1].ljust(18),staff_member[2].ljust(12),staff_member[3])
print("\n")


display_relationship_query = execute_join_member_leader()
related = execute_read_query(connection, display_relationship_query)

print('Member'.center(13), 'Cell'.center(22), 'Leader'.center(12),'\n__________________'.ljust(13),'____________'.ljust(12),'_____________________'.ljust(18))

switch = related[3][2]
for pod_member in related:
  print(pod_member[0].ljust(18),pod_member[1].ljust(12),pod_member[2],switch)
  if (switch != pod_member[2]):
    switch = pod_member[2]
    print('\n')
print("\n")


display_relationship_query = execute_join_leader_staff()


related = execute_read_query(connection, display_relationship_query)

print('Leader'.center(13), 'Cell'.center(22), 'Contact'.center(12),'\n__________________'.ljust(13),'____________'.ljust(12),'_____________________'.ljust(18))


for pod_leader in related:
  print(pod_leader[0].ljust(18),pod_leader[1].ljust(12),pod_leader[3])
print('\n')


######################### Drop Table Queries ##########################

drop_tables = input('Drop tables [y,n]? ')
if (drop_tables == 'y'):
  execute_query(connection,'drop table staff','Drop staff table')
  execute_query(connection,'drop table member', 'Drop member table')
  execute_query(connection,'drop table leader','Drop leader table') 