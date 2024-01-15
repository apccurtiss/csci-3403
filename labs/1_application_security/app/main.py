import binascii
from datetime import datetime
import json
from pathlib import Path
import random
import base64
import sqlite3

from flask import Flask, Response, abort, redirect, request, render_template, flash, g

app = Flask(__name__)
app.secret_key = "super secret"

from flask import g

DATABASE = 'db.sqlite3'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.template_filter()
def dateconversion(value):
    try:
        return value.strftime("%H:%M %m/%d/%y")
    except:
        return('No date found.')

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.context_processor
def load_user():
    return {
        "user": get_current_user()
    }

def encode_cookie(user_id):
    return base64.b64encode(json.dumps({"user_id": str(user_id)}).encode()).decode()

def get_current_user():
    try:
        user_id = json.loads(base64.b64decode(request.cookies["user_id"]))["user_id"]
    except (binascii.Error, KeyError, json.decoder.JSONDecodeError):
        return None

    return query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)

@app.route("/")
def index():
    user = get_current_user()
    if not user:
        return redirect("/login")

    posts = query_db(
        "SELECT username, picture_url, message, timestamp FROM posts INNER JOIN users ON posts.user_id = users.id "
        "ORDER BY timestamp DESC;")
    return render_template("index.html", posts=posts)

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"].lower()
    password = request.form["password"]

    user = query_db("SELECT id, password_was_reset FROM users WHERE username=? AND password=?", (username, password), one=True)
    if not user:
        flash("Invalid username or password", "danger")
        return redirect("/")

    else:
        resp = redirect("/")
        resp.set_cookie("user_id", encode_cookie(user["id"]), samesite="None", secure=True)
        return resp

@app.route("/logout", methods=["GET"])
def logout():
    resp = redirect("/")
    resp.delete_cookie("user_id")
    return resp

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"].lower()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if not username:
        flash("Username required", "danger")
        return redirect("/login")

    if password != confirm_password:
        flash("Passwords do not match", "danger")
        return redirect("/login")
    
    if query_db("SELECT * FROM users WHERE username=?", (username,), one=True):
        flash("User already exists", "danger")
        return redirect("/login")

    # Add the user to the database.
    db = get_db()
    user_id = db.execute("INSERT INTO users (username, picture_url, password) VALUES (?, ?, ?)", (username, "/static/profiles/user.png", password)).lastrowid
    db.commit()

    resp = redirect("/")
    resp.set_cookie("user_id", encode_cookie(user_id))
    return resp

@app.route("/reset_password")
def reset_password():
    return render_template("reset_password.html")

@app.route("/api/reset_request", methods=["POST"])
def send_reset_code():
    username = request.form["username"]
    user = query_db("SELECT * FROM users WHERE username=?", (username,), one=True)

    if not user:
        return json.dumps({
            "status": "failure",
            "error": "User does not exist"
        })
    else:
        reset_code = str(random.randint(0, 1000000))
        db = get_db()
        reset_id = db.execute("INSERT INTO reset_codes VALUES (?, ?)", (user["id"], reset_code)).lastrowid
        db.commit()
    
        return json.dumps({
            "status": "success",
            "user_id": user["id"],
            "reset_id": reset_id,
            "reset_code": reset_code
        })

@app.route("/api/reset_submit", methods=["POST"])
def submit_reset_code():
    reset_code = request.form["reset_code"]
    new_password = request.form["new_password"]

    user = query_db("SELECT user_id FROM reset_codes WHERE reset_code=?", (reset_code,), one=True)

    if user:
        db = get_db()
        db.execute("UPDATE users SET password=?, password_was_reset=1 WHERE id=?", (new_password, int(user["user_id"])))
        db.commit()
        complete_achievement("c", "You completed a challenge: Reset a user's password!") # non-publics
    else:
        flash("Incorrect code! Unable to reset password", "error")

    return redirect("/")

@app.route("/api/search/users", methods=["POST"])
def user_search():
    search = request.form["search"]
    return query_db("SELECT * FROM users WHERE username LIKE ?", (f"%{search}%",))

@app.route("/user/<user_id>")
def user_profile(user_id: int):
    user = query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)
    posts = query_db(
        "SELECT username, picture_url, message, timestamp FROM posts INNER JOIN users ON posts.user_id = users.id "
        "WHERE users.id=? "
        "ORDER BY timestamp DESC;", (user_id,))
    return render_template("user.html", user=user, posts=posts)

@app.route("/post", methods=["POST"])
def make_post():
    user = get_current_user()
    if not user:
        abort(Response("Must be logged in to make a post", 400))

    message = request.form.get("message", "")

    query_db("INSERT INTO posts VALUES (?, ?, ?)", (user["id"], message, datetime.now()))
    get_db().commit()


    return redirect("/")

if __name__ == "__main__":
    if not Path(DATABASE).is_file():
        init_db()
    app.run(host="0.0.0.0", port="80", debug=True)