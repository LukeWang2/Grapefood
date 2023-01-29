from flask import Flask, request
import radish as r

app = Flask(__name__)


@app.route("/user")
def user():
    action = request.args["action"]
    username = request.args.get("username").replace("%20", " ")
    interests = request.args.get("interests").replace("%20", " ")
    password = request.args.get("password")
    contact = request.args.get("contact")
    types = request.args.get("type")
    favRestaurants = request.args.get("restaurants").replace("%20", " ")
    favFoods = request.args.get("foods").replace("%20", " ")
    if action == "addinterest":
        r.storeInterests(username, interests)
    elif action == "getinterest":
        return r.getInterests(username)
    elif action == "adduser":
        r.registerUser(username, password, contact)
    elif action == "deleteuser":
        r.deleteUser(username)
    elif action == "recommendusers":
        return r.recommendUsers(username)
    elif action == "recommend":
        return r.generateRecommendation(types, favRestaurants, favFoods)
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
