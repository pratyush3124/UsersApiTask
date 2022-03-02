from flask import Flask
from flask import request
import json
import random
import string

my_app = Flask(__name__)

ENV = "DEV"

# env check
if ENV == "DEV":
    my_app.debug = True

# root
@my_app.route("/")
def home():
    return "Hi"

# query all users data
@my_app.route("/users/")
def get_users():
    with open("./users.json") as jsonFile:
        jsonFile = open("./users.json", "r")
        users = json.load(jsonFile)
        jsonFile.close()
        return {"users":users}

# query data of one user by userId
@my_app.route("/users/<userId>", methods=['GET'])
def get_user(userId):
    with open("./users.json") as jsonFile:
        users = json.load(jsonFile)
        for user in users:
            if user['_id'] == userId:
                return user
        return "No such user"

# update data of one user by userId
@my_app.route("/users/<userId>", methods=['POST'])
def modify_user(userId):
    jsonFile = open("./users.json", "r")
    users = json.load(jsonFile)
    jsonFile.close()

    for user in users:
        if user['_id'] == userId:
            if "active" in request.json.keys():
                user["active"] = request.json["active"]
            if "name" in request.json.keys():
                user["name"] = request.json["name"]
            if "email" in request.json.keys():
                user["email"] = request.json["email"]
            if "role" in request.json.keys():
                user["role"] = request.json["role"]
            if "password" in request.json.keys():
                user["password"] = request.json["password"]

            with open("./users.json", "w") as wf:
                json.dump(users, wf)
            return {"users":users}
    return "No such user"

# create new users
@my_app.route("/users/createUser", methods=['POST'])
def create_user():
    nu = {
        "_id" : gen_id(),
        "active" : request.json['active'],
        "name" : request.json['name'],
        "email" : request.json['email'],
        "role" : request.json['role'],
        "password" : request.json['password']
    }

    with open("./newUser.json", "w") as nuf:
        json.dump(nu, nuf)
    return "new user created"

# delete existing user with the given userId
@my_app.route("/users/<userId>", methods=['DELETE'])
def delete_user(userId):
    jsonFile = open("./users.json", "r")
    users = json.load(jsonFile)
    jsonFile.close()
    for user in users:
        if user['_id'] == userId:
            users.remove(user)
            with open("./deletedUsers.json", "w") as delu:
                json.dump(user, delu)
            with open("./users.json", "w") as writeFile:
                json.dump(users, writeFile)
            return "removed"
    return "no such user"

def gen_id():
    rand_id = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    return rand_id
