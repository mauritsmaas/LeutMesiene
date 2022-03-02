#!/usr/bin/env python3

import os
import time
from pyfiglet import Figlet
from clint.textui import colored
from flask_web_interface.app import startflask

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


if __name__ == "__main__":
    main()