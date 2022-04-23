#!/usr/bin/env python3
from json import JSONEncoder
import os
import sys
import time
from pyfiglet import Figlet
from clint.textui import colored
import sqlite3
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

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

    # to make it Json serializable
    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    type=self.type,
                    description=self.description,
                    usage=self.usage,
                    source=self.source,
                    cve=self.cve,
                    phase=self.phase,
                    attackos=self.attackos)


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
            startcommandline()
        elif c == '2':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print('Running flask')
            startflask()
        elif c == '0':
            print("Bye!")
            exit()
        os.system("clear")


def startcommandline():
    first = True
    while True:
        if first:
            os.system("clear")
            print(welcome("LeutMesiene"))
            print("Command line utility\n")
            first = False
        
        print("Please select an option: ")
        print("""\t1 : List items
        2 : Search items
        0 : Back""")
        c = input("\nEnter your choice : ")

        if c == '1':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print("Itemlist\n")
            i = getdbinfo()
            print(i)
        elif c == '2':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print('Search window')
        elif c == '0':
            return


def getdbinfo():
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')

        # Query to get all the items in db
        query = 'SELECT i.id, i.name, t.name, i.description, i.usage, i.source, i.cve, p.phase FROM items i \
                    INNER JOIN types t ON i.type_id = t.id \
                    INNER JOIN phases p ON i.phase_id = p.id '

        res = conn.execute(query)
        items = []
        for item in res.fetchall():
            # Query to get all attack oses by corresponsing item
            a_res = conn.execute('SELECT a.os FROM attack_oses a \
                                        JOIN item_attackos ia \
                                        ON a.id = ia.attackos_id \
                                        WHERE ia.item_id = ?',
                                (item[0],)).fetchall()
            attackoses = []
            for aos in a_res:
                attackoses.extend(aos)

            # Put all the data in object and list
            i = Item(item[0], item[1], item[2], item[3], item[4],
                    item[5], item[6], item[7], attackoses)
            items.append(i)
        return items
    except Exception as e:
        print(e)


def getitembyid(id):
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')

        # Query to get all the items in db
        query = 'SELECT i.id, i.name, t.name, i.description, i.usage, i.source, i.cve, p.phase FROM items i \
                    INNER JOIN types t ON i.type_id = t.id \
                    INNER JOIN phases p ON i.phase_id = p.id \
                    WHERE i.id = ? '

        res = conn.execute(query, id)
        i_res = res.fetchall()
        item = i_res[0]

        attackos_res = conn.execute('SELECT a.os FROM attack_oses a \
                                        JOIN item_attackos ia \
                                        ON a.id = ia.attackos_id \
                                        WHERE ia.item_id = ?',
                                    id).fetchall()
        attackoses = []
        for aos in attackos_res:
            attackoses.extend(aos)

        # print(attackoses)

        print(item[0])
        # Put all the data in object and list
        i = Item(item[0], item[1], item[2], item[3], item[4],
                item[5], item[6], item[7], attackoses)

        return i
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
