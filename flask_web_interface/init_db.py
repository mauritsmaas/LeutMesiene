#!/usr/bin/env python3
import sqlite3
import sys

connection = sqlite3.connect('database.db')

sql_file = open(sys.path[0] + '/dbstructure.sql')
sql_as_string = sql_file.read()
cur = connection.cursor()
cur.executescript(sql_as_string)


## Fill the types in DB
cur.execute("INSERT INTO types(name) VALUES (?)", ('command',))
cur.execute("INSERT INTO types(name) VALUES (?)", ('tool',))

## Fill the attack oses
cur.execute("INSERT INTO attack_oses (os) VALUES (?)", ('linux',))
cur.execute("INSERT INTO attack_oses (os) VALUES (?)", ('windows',))
cur.execute("INSERT INTO attack_oses (os) VALUES (?)", ('mac',))
cur.execute("INSERT INTO attack_oses (os) VALUES (?)", ('other',))

## Fill the phases
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('recon',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('scanning',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('initial foothold',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('privesc',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('maintain access',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('covering',))
cur.execute("INSERT INTO phases (phase) VALUES (?)", ('general',))

## Select the tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#cur.execute("SELECT * FROM atack_oses")
#cur.execute("SELECT * FROM phases")

res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res.fetchall():
    print(name[0])

connection.commit()
connection.close()

