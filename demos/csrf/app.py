from flask import Flask, request, redirect
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
    "s8fyq23p4volasi8fq2vgaf9wgv": "alex"
}

@app.route("/")
def index():
    index_html = open("index.html").read()
    index_html = index_html.replace("{username}", request.cookies.get("username"))

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
        response.set_cookie("username", user)
        return response
    else:
        return "Failure"

@app.route("/tweet", methods=["POST"])
def send_tweet():
    content = request.form["content"]
    user = request.cookies.get("username")
    tweets.append(f"{user}: {content}")

    return redirect("/")

app.run(port=80, debug=True)