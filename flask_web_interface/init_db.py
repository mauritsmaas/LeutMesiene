#!/usr/bin/env python3
import sqlite3

connection = sqlite3.connect('database.db')

## TODO: cant open it 
with open('dbstructure.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

## Fill the types in DB
cur.execute("INSERT INTO types (name) VALUES (?)", ('command',))
cur.execute("INSERT INTO types (name) VALUES (?)", ('tool',))

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

## Select the tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#cur.execute("SELECT * FROM atack_oses")
#cur.execute("SELECT * FROM phases")

for tablerow in cur.fetchall():
        table = tablerow[0]
        cur.execute("SELECT * FROM {t}".format(t = table))
        for row in cur:
            for field in row.keys():
                print(table, field, row[field])

connection.commit()
connection.close()

