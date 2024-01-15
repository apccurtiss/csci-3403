from pathlib import Path
from flask import Flask, Response, request, redirect
import random
import sqlite3

app = Flask(__name__)

def run_sql(query) -> sqlite3.Cursor:
    con = sqlite3.connect("database.db")
    results = con.execute(query)
    con.commit()
    return results

def init_database():
    run_sql("CREATE TABLE users (username TEXT, password TEXT)")
    run_sql("INSERT INTO users VALUES ('alex', 'swordfish'), ('carol', 'hunter2')")

    run_sql("CREATE TABLE sessions (username TEXT, session_token INTEGER)")

    run_sql("CREATE TABLE tweets (username TEXT, content TEXT)")
    run_sql("INSERT INTO tweets VALUES "
        "('alex', 'Did you know if you type your password it shows up as asterisks?'),"
        "('alex', 'Watch'),"
        "('alex', '*********'),"
        "('bob', 'hunter2'),"
        "('bob', 'How do I delete a post?')"
    )

@app.route("/")
def index():
    index_html = open("index.html").read()
    session_token = eval(request.cookies.get("session_token", "0"))

    user = run_sql(f"SELECT username FROM sessions WHERE session_token={session_token}").fetchone()
    if user:
        user = user[0]
    else:
        user = "Anonymous"

    tweets = run_sql("SELECT * FROM tweets").fetchall()
    tweet_html = "".join(f"<p>{username}: {tweet}</p>" for username, tweet in tweets)

    index_html = index_html.replace("{username}", user)
    index_html = index_html.replace("{tweets}", tweet_html)
    return index_html

@app.route("/login", methods=["GET"])
def login_page():
    return open("login.html").read()

@app.route("/login", methods=["POST"])
def log_user_in():
    username = request.form["username"]
    password = request.form["password"]

    username = run_sql("SELECT username FROM users WHERE username='" + username + "' AND password='" + password + "'").fetchone()

    if username:
        response = redirect("/")
        session_token = random.randint(0, 10000000000000000)
        run_sql("INSERT INTO sessions VALUES ('" + username[0] + "', '" + session_token + "')")
        response.set_cookie("session_token", session_token)
        return response
    else:
        return "Failure"

@app.route("/tweet", methods=["POST"])
def send_tweet():
    # Get user (or raise an error if the user does not exist)
    session_token = eval(request.cookies.get("session_token", "0"))

    user = run_sql("SELECT username FROM sessions WHERE session_token=" + session_token).fetchone()

    if user:
        user = user[0]
    else:
        user = "Anonymous"

    content = request.form["content"]
    run_sql("INSERT INTO tweets VALUES ('" + user + "', '" + content + "')")

    return redirect("/") 

if not Path("database.db").is_file():
    init_database()
app.run(port=80, debug=True)