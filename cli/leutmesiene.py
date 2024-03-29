#!/usr/bin/env python3
from json import JSONEncoder
import os
import sys
import re
import time
import jwt
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

class User(object):

    username = ""
    password = ""
    role = 0

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    # to make it Json serializable
    def to_dict(self):
        return dict(username = self.username,
                    password = self.password,
                    role = self.role)
    
    def __iter__(self):
        return self


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

    def create(self, name, type, description, usage, source, cve, phase, attackos):
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
            additemcli()
        elif c == '0':
            return

def additemcli():
    while True:
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
                            cve = input("CVE (can be blank) [format=cve-year-serialnumber] : ").lower()
                            if verify_cve(cve) == 1:
                                print("CVE given is good") 
                            elif verify_cve(cve) == 2:
                                print("CVE not given")
                                cve = 'na'
                            else:
                                print("CVE is in wrong format, make sure you use: cve-year-serialnumber")
                                break
                            phase = input("Phase (options= recon, scanning, initial foothold, privesc, maintain access, covering or general) : ")
                            match, phase = verify_phase(phase)
                            if match:
                                attackos = input("Attack OS(es) (options= linux, windows, mac or other) [if multiple split with comma ','] : ")
                                match_os, attackos_list = verify_attackos(attackos)
                                if match_os:
                                    ## TODO implement function for confirming data            
                                    add_item_db(name, type,description,usage,source,cve,phase, attackos_list)
                                else:
                                    print('Unable to match any OS on the input:', attackos)
                            else:
                                print("Could not match any phase on input:", phase)
                    else:
                        print('Please fill in the usage, try again')
                        break
                else:
                    print('Please fill in the description, try again')
                    break
            else:
                print("Type is not a command or tool, try again")
                break
        else:
            print("Please give the item a name!")
            break
        print(name, type,description,usage,source,cve, phase, attackos_list)
        break


## Verify fields section
def verify_id(id):
    try:
        if id > 0:
            return True
    except Exception:
        return False
    return False

def verify_input(text):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if re.findall("\w", text):
        return True
    elif(regex.search(text)):
        return True
    return False

def verify_type(type):
    if type.find('command') != -1:
        return "command"
    elif type.find('tool') != -1:
        return "tool"
    return False

def convert_type(type):
    if type == 'command':
        return 1
    elif type == 'tool':
        return 2

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
        return 1
    elif verify_input(cve) == False :
        return 2
    elif cve == 'na' or cve == 'NA':
        return 3
    return False

def verify_phase(phase):
    list = ['recon', 'scanning', 'initial foothold', 'privesc', 'maintain access', 'covering', 'general']
    for p in list:
        if (phase.lower()).find(p.lower()) != -1:
            return True, p
    return False, phase

def convert_phase(phase):
    if phase == 'recon':
        return 1
    elif phase == 'scanning':
        return 2
    elif phase == 'initial foothold':
        return 3
    elif phase == 'privesc':
        return 4
    elif phase == 'maintain access':
        return 5
    elif phase == 'covering':
        return 6
    elif phase == 'general':
        return 7

def verify_attackos(attackoses):
    attackos_values = ['linux', 'windows', 'mac', 'other']
    inputlist = attackoses.lower().split(',')
    for item in inputlist:
        item.lower()
        item.strip()
    final_list = []
    for a in attackos_values:
        for inputos in inputlist:
            if inputos.find(a) != -1:
                final_list.append(a)
    if final_list:
        return True, final_list
    else:
        return False, final_list

def verify_attack0s(attackos_list):
    list = ['linux', 'windows', 'mac', 'other']
    finallist = []
    for a in attackos_list:
        for os in list:
            if (a.lower()).find(os.lower()) != -1:
                finallist.append(os)
            return True, finallist
    return False

def convert_attackos(os):
    if os == 'linux':
        return 1
    elif os == 'windows':
        return 2
    elif os == 'mac':
        return 3
    elif os == 'other':
        return 4

def verification_all_values(id, name, type, description, usage, source, cve, attackos, phase):
    if verify_id(id):
        if verify_input(name):
            veri_type = verify_type(type)
            if veri_type != False:
                type = veri_type
                if verify_input(description):
                    if verify_input(usage):
                        if verify_site(source):
                            if verify_cve(cve) == 1:
                                cve = cve.lower()
                            elif verify_cve(cve) == 2:
                                cve = 'na'
                            elif verify_cve(cve) == 3:
                                cve = 'na'
                            else:
                                return False
                            if verify_phase(phase):
                                match_os, attackos_list = verify_attack0s(attackos)
                                if match_os:
                                    print("Done")
                                    print(name, type,description,usage,source,cve,phase, attackos)
                                    #everything checked
                                    print("NO ERRORS in VALIDATION")
                                    return True
                                else:
                                    print("ERROR in ATTACK OS", attackos)
                                    return False
                            else:
                                print("ERROR in PHASE", phase)
                                return False 
                        else:
                            print("ERROR in SOURCE", source)
                            return False   
                    else:
                        print("ERROR in USAGE", usage)
                        return False
                else:
                    print("ERROR in DESCRIPTION", description)
                    return False    
            else:
                print("ERROR in TYPE", type)
                return False
        else:
            print("ERROR in NAME", name)
            return False
    else:
        print("ERROR in ID", id)
        return False
            

def verification_values_new_item(name, type, description, usage, source, cve, attackos, phase):
    if verify_input(name):
        veri_type = verify_type(type)
        if veri_type != False:
            type = veri_type
            if verify_input(description):
                if verify_input(usage):
                    if verify_site(source):
                        if verify_cve(cve) == 1:
                            cve = cve.lower()
                        elif verify_cve(cve) == 2:
                           cve = 'na'
                        elif verify_cve(cve) == 3:
                            cve = 'na'
                        else:
                            return False
                        if verify_phase(phase):
                            match_os, attackos_list = verify_attack0s(attackos)
                            if match_os:
                                print("Done")
                                print(name, type,description,usage,source,cve,phase, attackos)
                                print("NO ERRORS in VALIDATION")
                                return True
                            else:
                                print("ERROR in ATTACK OS", attackos)
                                return False
                        else:
                            print("ERROR in PHASE", phase)
                            return False 
                    else:
                        print("ERROR in SOURCE", source)
                        return False   
                else:
                    print("ERROR in USAGE", usage)
                    return False
            else:
                print("ERROR in DESCRIPTION", description)
                return False    
        else:
            print("ERROR in TYPE", type)
            return False
    else:
        print("ERROR in NAME", name)
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


def getitemid_byname(name):
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')

        # Query to get all the items in db
        query = 'SELECT MAX(id) FROM items \
                    WHERE name = ? '

        res = conn.execute(query, (name,))
        i_res = res.fetchone()

        return i_res[0]
    except Exception as e:
        print(e)

def getitembyid(id):
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')
        cur = conn.cursor()
        # Query to get item by ID in db
        query = """ SELECT i.id, i.name, t.name, i.description, i.usage, i.source, i.cve, p.phase FROM items i \
                    INNER JOIN types t ON i.type_id = t.id \
                    INNER JOIN phases p ON i.phase_id = p.id \
                    WHERE i.id = ? """
        print('Succes until first execute')
        res = cur.execute(query, (id,))
        
        i_res = res.fetchall()
        print("I_RES:",i_res)
        item = i_res[0]

        query_attackos = """ SELECT a.os FROM attack_oses a \
                                        JOIN item_attackos ia \
                                        ON a.id = ia.attackos_id \
                                        WHERE ia.item_id = ? """

        attackos_res = cur.execute(query_attackos, (id,)).fetchall()
        attackoses = []
        for aos in attackos_res:
            attackoses.extend(aos)

        # Put all the data in object and list
        i = Item(item[0], item[1], item[2], item[3], item[4],
                item[5], item[6], item[7], attackoses)
        
        return i
    except Exception as e:
        print(e)

def add_item_db(name, type,description,usage,source,cve,phase, attackos_list):
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')
        cur = conn.cursor()

        # Insert items
        cur.execute("INSERT INTO items (name, type_id, description, usage, source, cve, phase_id) VALUES (?,?,?,?,?,?,?)", 
        (name, convert_type(type), description, usage, source ,cve, convert_phase(phase) ))

        conn.commit()

        # Check for new id
        item_id = getitemid_byname(name)

        # Insert many-to-many
        for os in attackos_list:
            cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (item_id, convert_attackos(os)))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def update_item(id, name, type, description, usage, source, cve, attackos, phase):
    if verification_all_values(id, name, type, description, usage, source, cve, attackos, phase):
        #try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')
        cur = conn.cursor()

        # Update item
        cur.execute('UPDATE items \
                    SET name = ?, \
                        type_id = ?, \
                        description = ?, \
                        usage = ?, \
                        source = ?, \
                        cve = ?, \
                        phase_id = ? \
                    WHERE id = ?' , 
        (name, convert_type(type), description, usage, source ,cve, convert_phase(phase), id ))

        conn.commit()
        # Delete old many-to-many
        cur.execute('DELETE FROM item_attackos \
                    WHERE item_id = ?', (id,))
        conn.commit()

        # Insert many-to-many
        for os in attackos:
            cur.execute("INSERT INTO item_attackos (item_id, attackos_id) VALUES (?, ?)", (id, convert_attackos(os)))
        conn.commit()
        conn.close()
        #except Exception as e:
            #print(e)
    
    print('updated the item in DB')

def deleteItem(id):
    try:
        # Make connection with db file
        conn = sqlite3.connect(sys.path[0] + '/cli/database.db')
        cur = conn.cursor()

        # Delete item in item table
        cur.execute('DELETE FROM items \
                    WHERE id = ?', (id,))
        conn.commit()

        # Delete many-to-many relations
        cur.execute('DELETE FROM item_attackos \
                    WHERE item_id = ?', (id,))
        conn.commit()
        
    except Exception as e:
        print(e)

## User handling

users = [User("test", "test",0), User("aaa", "aaa",1)]

user_token_dict = {}

def login_user(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return False

## JWT handling

SECRET_KEY = "CompuFun"

def createJWTToken(user):
    payload = {
        "username": user.username,
        "role" : user.role,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(seconds=3000)
    }
    encoded_data = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")
    return encoded_data

def validate_jwttoken(token):
    try:
        decode_data = jwt.decode(jwt=token, \
                            key=SECRET_KEY, algorithms="HS256")
        print(decode_data)
        return True, token
    except Exception as e:
        message = f"Token is invalid --> {e}"
        print({"message": message})
        return False, message 

def renew_token(token):  
    username = get_keys_from_value(token)[0]
    print("DIT IS DE USER", username)
    
    account = ''
    for u in users:
        if username == u.username:
            account = u

    payload = {
        "username": account.username,
        "role" : account.role,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
    }
    new_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    couple_user_token(account.username, new_token)
    return new_token

def get_keys_from_value(val):
    return [k for k, v in user_token_dict.items() if v == val]

def get_token(header):
    PREFIX = 'Bearer'
    bearer, _, token = header.partition(' ')
    if bearer != PREFIX:
        raise ValueError('Invalid token')

    return token

def couple_user_token(username, token):
    user_token_dict.update({username : token}) 
    print(user_token_dict)

def check_user_role(token):
    decode_data = jwt.decode(token, options={"verify_signature": False})
    return decode_data['role']

if __name__ == "__main__":
    main()
