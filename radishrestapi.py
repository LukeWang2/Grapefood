from flask import Flask, request
import radish as r

app = Flask(__name__)


@app.route("/user")
def user():
    action = request.args["action"]
    username = request.args.get("username")
    interests = request.args.get("interests")
    password = request.args.get("password")
    contact = request.args.get("contact")
    if action == "addinterest":
        r.storeInterests(username, interests)
    elif action == "getinterest":
        return r.getInterests(username)
    elif action == "adduser":
        r.registerUser(username, password, contact)
