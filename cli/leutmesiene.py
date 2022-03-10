#!/usr/bin/env python3

import os
import sys
import time
from pyfiglet import Figlet
from clint.textui import colored
import sqlite3

p = os.path.abspath('.')
sys.path.insert(1, p)
from flask_web_interface.app import *

class Item(object):
    id = 0
    name = ""
    type = ""
    description = ""
    usage = ""
    source = ""
    cve = ""
    attackos = []
    phase = ""

    def __init__(self, id, name, type, description, usage, source, cve, phase, attackos):
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.usage = usage
        self.source = source
        self.cve = cve
        self.attackos = attackos
        self.phase = phase
    
    def set_attackos(self, attackos):
        self.attackos.append(attackos)

def welcome(text):
    result = Figlet()
    return colored.green(result.renderText(text))

def main():
   while True:
        os.system("clear")
        print(welcome("LeutMesiene"))
        print("The knowledge/cheatsheet of a lazy hacker\n")
        print("Please select an option ")
        print("""\t1 : Continue in commandline
        2 : Start web interface
        0 : Exit""")
        c = input("\nEnter your choice : ") 

        if c == '1':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print("This is not implemented jet\n")
            time.sleep(5)
        elif c == '2':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print('Running flask')
            startflask()
        elif c == '0':
            print("Bye!")
            exit()
        os.system("clear")

def getdbinfo():
    try:
        #Make connection with db file
        conn = sqlite3.connect('database.db')

        #Query to get all the items in db
        query = 'SELECT i.id, i.name, t.name, i.description, i.usage, i.source, i.cve, p.phase \
            FROM items i \
                INNER JOIN types t ON i.type_id = t.id \
                INNER JOIN phases p ON i.phase_id = p.id '

        res = conn.execute(query)
        items = []
        for item in res.fetchall():
            #Query to get all attack oses by corresponsing item
            a_res = conn.execute('SELECT a.os FROM attack_oses a \
                                    JOIN item_attackos ia \
                                    ON a.id = ia.attackos_id \
                                    WHERE ia.item_id = ?',
                                    (item[0],)).fetchall()
            attackoses = []
            for aos in a_res:
                attackoses.extend(aos)
            
            #Put all the data in object and list
            i = Item(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7], attackoses)
            items.append(i)
        return items
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #getdbinfo()
    main()