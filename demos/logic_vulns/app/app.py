from time import sleep
from typing import Optional
from flask import Flask, session, flash

app = Flask(__name__)
app.secret_key = "super secret"

def get_logged_in_user() -> Optional[str]:
    return session.get("username")

def login_user(username: str) -> None:
    session["username"] = username

def logout_user() -> None:
    del session["username"]

# Alias the name to make it easier to understand.
def show_message(message):
    flash(message, "success")

def show_error(message):
    flash(message, "danger")

def send_text_code(user, text_code) -> None:
    # If we had the ability to send text codes, this would do it.
    pass

def ship_items() -> None:
    # If we had the ability to ship purchases to people, this would do it.
    pass

def calculate_cart_total(cart, item_database) -> int:
    total = 0
    for item, quantity in cart.items():
        total += item_database[item]["price"] * quantity
    return total