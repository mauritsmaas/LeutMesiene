#!/usr/bin/env python3
import os
import sys
import json
import inspect
import datetime
import re
from traceback import print_tb
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from flask import make_response

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from cli.leutmesiene import *

app = Flask(__name__,
            static_folder = "../frontend/dist/static",
            template_folder = "../frontend/dist")

# Handles the Cross Origin Resource Sharing, https://flask-cors.readthedocs.io/en/latest/
cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5001", "http://127.0.0.1:5001", "http://localhost:8081", "http://127.0.0.1:8081"]}})

#Catch the different paths and use the vue-router
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/items', methods=['GET'])
@cross_origin()
def all_items():
    items = getdbinfo()
    return jsonify({
        'items': [i.to_dict() for i in items]
    })

@app.route('/api/item/<id>/update', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
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

    # Validates the token in auth header
    result = validate_token(request)
    ## If valid token do update, else return not updated item with error message (666)
    if check_jwt_pattern(result):
        update_item(item_id, name, type, description, usage, source, cve, attackos, phase)
        
        item_new = getitembyid(item_id)

        if (result == get_token(request.headers["Authorization"])):
            return jsonify({
            'item': item_new.to_dict()
            })
        else:
            return jsonify({
                'item': item_new.to_dict(),
                'token': result
            }) 
    else:
        return app.make_response((result, 666))


@app.route('/api/item/add', methods=['POST'])
@cross_origin()
def item_add():
    req = request.get_json()
    print(req)

    # Validates the token in auth header
    result = validate_token(request)
    ## If valid token do update, else return not updated item with error message (666)
    if check_jwt_pattern(result):
        if(verification_values_new_item(req["name"], req["type"],req["description"], req["usage"], req["source"], req["cve"], req["attackos"], req["phase"])):
            print("check")
            add_item_db(req["name"], req["type"],req["description"], req["usage"], req["source"], req["cve"], req["phase"], req["attackos"])
            
            item_new = getitembyid(getitemid_byname(req["name"]))
            print(item_new)
            if (result == get_token(request.headers["Authorization"])):
                return jsonify({
                'item': item_new.to_dict()
                })
            else:
                return jsonify({
                    'item': item_new.to_dict(),
                    'token': result
                })
        else:
            return app.make_response(("Syntax error", 666))   
    return app.make_response((result, 666))
    

@app.route('/api/item/<id>', methods=['GET'])
@cross_origin()
def item_details(id):
    item = getitembyid(id)
    print(item.to_dict())
    return jsonify({
        'item': item.to_dict()
    })

@app.route('/api/item/<id>/delete', methods=['DELETE'])
@cross_origin()
def item_delete(id):
    result = validate_token(request)
    ## If valid token do delete, else return not delete item with error message (666)
    if check_jwt_pattern(result):
        if (check_user_role(result) < 1):
            deleteItem(id)
            if (result == get_token(request.headers["Authorization"])):
                return jsonify({
                    'message': "Item with ID "+id+" is deleted"
                })
            else:
                return jsonify({
                    'message': "Item with ID "+id+" is deleted",
                    'token': result
                })
        else:
            return app.make_response(("You are not allowed to do this action", 403))
    return app.make_response((result, 666))

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
            "token": token 
            #"token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOjEsImV4cCBLAI6MTY2MDg5Njk1NH0.H8zPwn_Msgq27xoE5_PeP_oJMYXjwPuOh-h6ibXXXLg" #INVALID SIGNATURE
            #"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOjEsImV4cCI6MTY2MTE1MjY0NH0.Tw4UmWlz-cJ6ALQAWy9ILExysaESA7LsdpaidsiN-xA" #EXPIRED TOKEN
        })
    return app.make_response(("Login failed", 666))

## Functions that are not an API but essential for validation of authorization
def validate_token(request):
    token = get_token(request.headers["Authorization"])
    if check_jwt_pattern(token):
        bool, result = validate_jwttoken(token)
        print("VALIDATIE BACKEND", bool, result, token)
        if bool == True:
            return result
        if 'expired' in result:
            try:
                newtoken =  renew_token(token)
                return newtoken
            except Exception as e:
                message = f"Token is invalid --> session cannot be validated"
                return message
        return result
    return False
    
def check_jwt_pattern(input):
    try:
        pattern = re.compile("^[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_.+/=]*$")
        if pattern.match(input):
            return True
        return False
    except Exception as e:
        message = f"Token is invalid --> {e}"
        print({"message": message})
        return message 
    


def startflask():
    app.run(port=5001)

if __name__ == "__main__":
    startflask()
