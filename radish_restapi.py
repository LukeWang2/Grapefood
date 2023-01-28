from flask import Flask
import radish as r
from werkzeug.security import generate_password_hash, check_password_hash
import os

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/api")
def test():
    return "foo"
