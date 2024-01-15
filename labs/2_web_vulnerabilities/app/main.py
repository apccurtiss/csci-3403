import logging
import os
from pathlib import Path
import random
import string
import time
from uuid import uuid4
from flask import Flask, Response, abort, redirect, request, render_template, flash, g
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret"

from flask import g

DATABASE = 'db.sqlite3'
SESSIONS = {}

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        db.create_function("SLEEP", 1, time.sleep)
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


def get_current_user():
    session_token = request.cookies.get("session_token")

    user_id = SESSIONS.get(session_token)
    if not user_id:
        return None

    return query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)

@app.route("/")
def index():
    products = query_db("SELECT * FROM products WHERE unlisted=False")
    return render_template("index.html", products=products)

@app.route("/search")
def search():
    search_query = request.args.get("query", "")

    sql_query = f"SELECT name, description, picture_url, price FROM products WHERE name LIKE '%{search_query}%' AND unlisted=False"
    if "from users" in sql_query.lower():
        return render_template("index.html", search_query=search_query, error=f"Cannot read from the users table here (you will need to use a different input for Blind SQL portion)")

    try:
        products = query_db(sql_query)
    except sqlite3.OperationalError as e:
        return render_template("index.html", search_query=search_query, error=f"{sql_query}: {e}")

    return render_template("index.html", search_query=search_query, products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql_query = f"SELECT id, username FROM users WHERE username='{username}' AND password='{password}'"
    try:
        user = query_db(sql_query, one=True)
    except sqlite3.OperationalError as e:
        return render_template("login.html", error=f"{sql_query}: {e}")

    if not user:
        return render_template("login.html", error="Invalid username or password")

    resp = redirect("/")
    session_token = str(uuid4())
    SESSIONS[session_token] = user["id"]
    resp.set_cookie("session_token", session_token, httponly=False)
    return resp

@app.route("/logout", methods=["GET"])
def logout():
    resp = redirect("/")
    resp.delete_cookie("session_token")
    return resp

if __name__ == "__main__":
    if not Path(DATABASE).is_file():
        init_db()
    app.run(host="0.0.0.0", port="80", debug=True)