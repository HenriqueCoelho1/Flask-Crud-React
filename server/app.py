from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_react'
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


@app.route("/", methods=["GET"])
def index():
    return {
        "name": "Testing"
    }


if __name__ == "__main__":
    app.run(debug=True)
