#!/usr/bin/env python3
import os
import sys
from flask import Flask, render_template

p = os.path.abspath('../')
sys.path.insert(1, p)
from cli.leutmesiene import *

app = Flask(__name__,
            static_folder = "../frontend/dist/static",
            template_folder = "../frontend/dist")

#Catch the different paths and use the vue-router
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/test")
# def indextest():
#     items = getdbinfo()
#     return render_template('basic_table.html', title='Basic Table',
#                            items=items)

def startflask():
    app.run()

if __name__ == "__main__":
    startflask()
