#!/usr/bin/env python3
import os
import sys
import json
import inspect
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from cli.leutmesiene import *

app = Flask(__name__,
            static_folder = "../frontend/dist/static",
            template_folder = "../frontend/dist")

# Handles the Cross Origin Resource Sharing, https://flask-cors.readthedocs.io/en/latest/
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#Catch the different paths and use the vue-router
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/items', methods=['GET'])
def all_items():
    items = getdbinfo()
    return jsonify({
        'items': [i.to_dict() for i in items]
    })

@app.route('/api/item/<id>/update', methods=['POST'])
def item_update(id):
    req = request.get_json()
    item_id = req['id']
    name = req['name']
    type = req['type']
    description = req['description']
    usage = req['usage']
    source = req['source']
    cve = req['cve']
    attackos = req['attackos']
    phase = req['phase']

    print(item_id)

    update_item(item_id, name, type, description, usage, source, cve, attackos, phase)
    
    item_new = getitembyid(item_id)
    print(item_new)
    return jsonify({
        'item': item_new.to_dict()
    })

@app.route('/api/item/<id>', methods=['GET'])
def item_details(id):
    item = getitembyid(id)
    print(item.to_dict())
    return jsonify({
        'item': item.to_dict()
    })

def startflask():
    app.run()

if __name__ == "__main__":
    startflask()
