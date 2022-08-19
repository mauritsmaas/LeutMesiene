#!/usr/bin/env python3
import os
import sys
import json
import inspect
import datetime
import re
from traceback import print_tb
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask import make_response

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
    print(req)

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

    # Validate the token in header
    # TODO: handle different results if JWT is not correct
    # TODO: update functionality only execute based on the input in dictionary
    # TODO: renew JWT also in the dictionary
    result = validate_token(request)
    print(check_jwt_pattern(result))


    update_item(item_id, name, type, description, usage, source, cve, attackos, phase)
    
    item_new = getitembyid(item_id)

    return jsonify({
        'item': item_new.to_dict()
    })
    

@app.route('/api/item/add', methods=['POST'])
def item_add():
    req = request.get_json()
    print(req)
    if(verification_values_new_item(req["name"], req["type"],req["description"], req["usage"], req["source"], req["cve"], req["attackos"], req["phase"])):
        print("check")
        add_item_db(req["name"], req["type"],req["description"], req["usage"], req["source"], req["cve"], req["phase"], req["attackos"])
        
        item_new = getitembyid(getitemid_byname(req["name"]))
        print(item_new)
        return jsonify({
            'item': item_new.to_dict()
        })
    else:
        print("failed")
        return app.make_response(("Syntax not right", 666))   
    

@app.route('/api/item/<id>', methods=['GET'])
def item_details(id):
    item = getitembyid(id)
    print(item.to_dict())
    return jsonify({
        'item': item.to_dict()
    })

@app.route('/api/item/<id>/delete', methods=['DELETE'])
def item_delete(id):
    deleteItem(id)
    return app.make_response(("Item with ID "+id)+" is deleted")

@app.route('/api/login', methods=['POST'])
def login():
    req = request.get_json()

    ## Logic to login 
    result = login_user(req["username"], req["password"])

    if result != False :
        token = createJWTToken(result)
        couple_user_token(result.username, token)
        return jsonify({
            "user": result.username,
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOjEsImV4cCBLAI6MTY2MDg5Njk1NH0.H8zPwn_Msgq27xoE5_PeP_oJMYXjwPuOh-h6ibXXXLg"
        })
    return app.make_response(("Login failed", 666))

# @app.route('/api/validate', methods=['POST'])
def validate_token(request):
    token = get_token(request.headers["Authorization"])
    bool, result = validate_jwttoken(token)
    print("VALIDATIE BACKEND", bool, result, token)
    if bool == True:
        return result
    if 'expired' in result:
        newtoken =  renew_token(request["user"])
        return newtoken
    return result
    
def check_jwt_pattern(input):
    pattern = re.compile("^[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_.+/=]*$")
    if pattern.match(input):
        print("IT IS JWT")
        return True
    return False


def startflask():
    app.run(port=5001)

if __name__ == "__main__":
    startflask()
