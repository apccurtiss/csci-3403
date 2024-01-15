from flask import Flask, Response, request, redirect
import random

app = Flask(__name__)

users = {
    "alex": "swordfish",
    "alice": "password",
    "bob": "hunter2",
    "carol": "cats",
    "student": "csci3403!",
}

tweets = [
    "alex: Did you know if you type your password it shows up as asterisks?",
    "alex: Watch",
    "alex: *********",
    "bob: hunter2",
    "bob: How do I delete a post?",
]

sessions = {
}

@app.route("/")
def index():
    index_html = open("index.html").read()
    user = sessions.get(request.cookies.get("session_token"), "None")
    index_html = index_html.replace("{username}", user)

    tweet_html = "".join(f"<p>{tweet}</p>" for tweet in tweets)
    index_html = index_html.replace("{tweets}", tweet_html)
    return index_html

@app.route("/login", methods=["GET"])
def login_page():
    return open("login.html").read()

@app.route("/login", methods=["POST"])
def log_user_in():
    user = request.form["username"]
    password = request.form["password"]

    if users[user] == password:
        response = redirect("/")
        session_token = str(random.randint(0, 10000000000000000))
        sessions[session_token] = user
        response.set_cookie("session_token", session_token)
        return response
    else:
        return "Failure"

@app.route("/tweet", methods=["POST"])
def send_tweet():
    # Get user (or raise an error if the user does not exist)
    user = "test"
    # user = sessions.get(request.cookies.get("session_token"))
    # if not user:
    #     return Response("Must be logged in to Tweet", 403)

    content = request.form["content"]
    tweets.append(f"{user}: {content}")

    return redirect("/")

app.run(port=80, debug=True)