from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os
import json
import datetime

load_dotenv(override=True)

app = Flask(__name__)
root_db = os.getenv("ROOT")
pass_db = os.getenv("PASS")
localhost_db = os.getenv("LOCALHOST")
postgree_port_db = os.getenv("POSTGREE_PORT")
name_db = os.getenv("DATABASE_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{root_db}:{pass_db}@{localhost_db}:{postgree_port_db}/{name_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "usr"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, name, address):
        self.username = username
        self.email = email
        self.name = name
        self.address = address

    def to_json(self):
        return {"id": self.id,
                "username": self.username,
                "name": self.name,
                "email": self.email,
                "address": self.address}

# GET ALL USERS


@app.route("/users", methods=["GET"])
def select_users():
    get_all_users = User.query.all()
    get_all_users_json = [user.to_json() for user in get_all_users]
    return set_response(200, "users", get_all_users_json)
    # return Response(json.dumps(get_all_users_json))


# GET USER BY ID
@app.route("/users/<id>", methods=["GET"])
def select_user_by_id(id):
    get_user_by_id = User.query.filter_by(id=id).first()

    # IS NOT NECESSARY TO PASS A FOR LOOP BECAUSE RETURN JUST 1 VALUE
    get_user_by_id_json = get_user_by_id.to_json()

    return Response(200, "user", get_user_by_id_json)


# CREATE A USER
@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()

    try:
        user = User(username=body["username"],
                    name=body["name"],
                    email=body["email"],
                    address=body["address"])
        db.session.add(user)
        db.session.commit()

        return set_response(201, "user", user.to_json(), "Created with success")
    except Exception as e:
        print(e)
        return set_response(400, "user", {}, "Error to register")


# UPDATE A USER
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if("username" in body):
            user.username = body["username"]

        if("name" in body):
            user.name = body["name"]

        if("address" in body):
            user.address = body["address"]

        db.session.add(user)
        db.session.commit()

        return set_response(201, "user", user.to_json(), "Updated with success")

    except Exception as e:
        print(e)
        return set_response(400, "user", {}, "Error to update")


@app.route("/users/<id>", methods=["DELETE"])
def remove_user(id):
    user = User.query.filter_by(id=id).first()

    try:
        db.session.delete(user)
        db.session.commit()
        return set_response(200, "user", user.to_json(), "Delted with success")

    except Exception as e:
        print(e)
        return set_response(400, "user", {}, "Error to delete")


def set_response(status, content_name, content, message=False):
    body = {}
    body[content_name] = content

    if(message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
