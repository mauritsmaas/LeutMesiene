#!/usr/bin/env python3
from json import JSONEncoder
import os
import sys
import re
import time
from pyfiglet import Figlet
from clint.textui import colored
from tabulate import tabulate
import sqlite3
import inspect
from prettytable import PrettyTable
from textwrap import fill

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
    
    def __iter__(self):
        return self
    
    

    # def __iter__(self):
    #     return iter(self.id,
    #             self.name,
    #             self.type,
    #             self.description,
    #             self.usage,
    #             self.source,
    #             self.cve,
    #             self.phase,
    #             self.attackos)

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
        3 : Add item
        0 : Back""")
        c = input("\nEnter your choice : ")

        if c == '1':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print("Itemlist\n")
            print_allitems()
        elif c == '2':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print('Search window')
        elif c == '3':
            os.system("clear")
            print(welcome("LeutMesiene"))
            print('Adding item')
            #verify_site("http://nu.nl")
            additemcli()
        elif c == '0':
            return

def additemcli():
    name = input("\nName : ")
    if verify_input(name):
        type = input("Type [tool/command] : ")
        veri_type = verify_type(type)
        if veri_type != False:
            type = veri_type
            description = input("Description (optional keywords) : ")
            if verify_input(description):
                usage = input("Usage : ")
                if verify_input(usage):
                    source = input("Source/site : ")
                    if verify_site(source):
                        cve = input("CVE (can be blank) [format=cve-year-serialnumber] : ")
                        if verify_cve(cve.lower()):
                            cve = cve.lower()
                            print("CVE good")
                            ## IMPLEMENT no cve input with NA 
                        else:
                            print("CVE is in wrong format, make sure you use: cve-year-serialnumber")
                else:
                    print('Please fill in the usage, try again')
            else:
                print('Please fill in the description, try again')
        else:
            print("Type is not a command or tool, try again")
            return

    print(name, type,description,usage,source)
    # description = input("Description (optional keywords) : ")
    # usage = input("Usage : ")
    # source = input("Source/site : ")
    # cve = input("CVE (can be blank) : ")
    # phase = input("Phase (options= recon, scanning, initial foothold, privesc, maintain access, covering or general) : ")
    # attackos = input("Attack OS(es) (options= linux, windows, mac or other) [if multiple split with comma ','] : ")
    # print(name, type, description, usage, source, cve, phase, attackos)


## Verify fields section
def verify_input(text):
    if re.findall("\w", text):
        return True
    return False

def verify_type(type):
    if type.find('command') != -1:
        return "command"
    elif type.find('tool') != -1:
        return "tool"
    return False

def verify_site(site):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
        r'localhost|' #localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, site):
        return True
    else:
        return False

def verify_cve(cve):
    if re.findall("\Acve-[0-9][0-9][0-9][0-9]-", cve):
        return True
    return False

def print_allitems():
    head = ["id", "name", "type", "description", "usage", "source", "cve", "phase", "attack_oses"]
    items = getdbinfo()

    ## Tabulate solution
    ITER_items=[]
    for item in items:
        ITER_items.append([item.id, item.name, item.type,  fill(item.description, width=30), fill(item.usage, width=30), fill(item.source, width=30), item.cve, item.phase, item.attackos])
    print(tabulate(ITER_items, headers=head, tablefmt="fancy_grid"))

    ## PrettyTable solution
    # table = PrettyTable(head, align='c')
    # items = getdbinfo()
    # for item in items:
    #     table.add_row([item.id, item.name, item.type, fill(item.description, width=30), fill(item.usage, width=30), fill(item.source, width=30), item.cve, item.phase, item.attackos])
    # print(table.get_string(border=True))

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

        print(item[0])
        # Put all the data in object and list
        i = Item(item[0], item[1], item[2], item[3], item[4],
                item[5], item[6], item[7], attackoses)

        return i
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
