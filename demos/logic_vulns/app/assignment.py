import random
from app import *
from flask import request, render_template, redirect

"""This database stores each item that users can buy."""
item_database = {
    "One penny": {
        "price": 0.01,
        "icon": "penny.jpg",
        "description": "One penny",
    },
    "Some socks": {
        "price": 4.99,
        "icon": "sock.jpg",
        "description": "A pair of socks",
    },
    "A laptop": {
        "price": 1099.99,
        "icon": "laptop.jpg",
        "description": "A brand new laptop!",
    }
}

"""This database stores all of the users."""
user_database = {
    "admin": {
        "username": "admin",
        "password": "swordfish",
        "account_balance": 10,
        "cart": {},
        "purchase_history": [],
    }
}

"""This code displays the main page."""
@app.route("/")
def index():
    username = get_logged_in_user()
    user = user_database.get(username)

    return render_template(
        "index.html",
        user=user,
        items=item_database)

"""This code is run every time a user tries to log in."""
@app.route("/login")
def login():
    username = request.args["username"]
    password = request.args["password"]

    user = user_database.get(username)

    if not user:
        show_error("Username does not exist")
    elif password != user["password"]:
        show_error("Invalid password")
    else:
        # Successfully log the user in.
        login_user(username)

    # After logging in, send the user back to the home page.
    return redirect("/")

"""This code is run every time a user tries to sign up with a new account."""
@app.route("/create_account")
def create_account():
    username = request.args["username"]
    password = request.args["password"]
    confirm_password = request.args["confirm_password"]

    if not username:
        show_error("Username required")
        return redirect("/")

    if password != confirm_password:
        show_error("Passwords do not match")
        return redirect("/")
    
    # Add the user to the database.
    user_database[username] = {
        "username": username,
        "password": password,
        "account_balance": 10,
        "cart": {},
        "purchase_history": [],
    }

    show_message("Congratulations! You have been given a free $10 for signing up!")

    # Log the user into their new account.
    login_user(username)

    # After creating an account, send the user to the home page.
    return redirect("/")

"""This code is run every time a user tries to log out."""
@app.route("/logout")
def logout():
    # Log the user out and send them back to the home page.
    logout_user()
    return redirect("/")

"""This code is called when a user adds an item to their cart."""
@app.route("/add_to_cart")
def add_to_cart():
    item_name = request.args["item_name"]
    quantity = int(request.args["quantity"])

    username = get_logged_in_user()
    user = user_database[username]

    # If they already have that item in their cart, add to the quantity, otherwise add a new entry to the cart
    if item_name in user["cart"]:
        user["cart"][item_name] += quantity
    else:
        user["cart"][item_name] = quantity
    
    # Inform the user of the successful total
    cart_total = calculate_cart_total(user["cart"], item_database)
    show_message(f"Added {quantity} item(s) to cart (total: ${cart_total:3.2f})")

    return redirect("/") 

"""This code displays the cart of a specific user."""
@app.route("/cart")
def view_cart():
    username = request.args["username"]
    user = user_database[username]

    cart_total = calculate_cart_total(user["cart"], item_database)

    return render_template("cart.html", cart=user["cart"], items=item_database, total=cart_total, user=user)

"""This code is run every time a user checks out."""
@app.route("/checkout")
def purchase():
    username = request.args["username"]
    user = user_database[username]

    # Calculate how much is in the user's cart
    total = calculate_cart_total(user["cart"], item_database)

    # Make sure the user has enough money
    if total > user["account_balance"]:
        show_error(f"Insufficient funds: you have ${user['account_balance']}")
        return redirect(f"/cart?username={username}")

    # If users have enough money in their account, subtract that from the balance
    if total < user["account_balance"]:
        user["account_balance"] -= total

    # Ship the users their new items!
    ship_items()

    # Clear user's cart and let them know that the purchase was successful
    user["cart"] = {}
    show_message(f"Purchase successful! Remaining balance: ${user['account_balance']:3.2f}")
    
    return redirect("/")

"""This displays the reset password page, where users enter which username they want to reset."""
@app.route("/reset_password")
def reset_password():
    return render_template("reset_password.html")

"""This code is called when a user tries to reset their password."""
@app.route("/send_reset_code")
def send_reset_code():
    username = request.args["username"]
    user = user_database.get(username)

    if not user:
        # If the user does not exist, send the user back to the password reset page.
        show_error("User does not exist")
        return redirect("/reset_password")

    # Pick a super random string to be the reset code
    password_reset_code = str(random.randint(0, 1000000))

    # Send a text with that code to the user's phone
    send_text_code(user, password_reset_code)

    # Record the random code in the user database
    user["password_reset_code"] = password_reset_code

    # Send the user to the page where they can enter the code they should have received
    return render_template("submit_reset_code.html", username=username)

"""This code is called when a user submits a password reset code."""
@app.route("/submit_reset_code")
def submit_reset_code():
    username = request.args["username"]
    reset_code = request.args["reset_code"]
    new_password = request.args["new_password"]

    user = user_database[username]

    # Verify that the reset code the user entered matches the one in the database
    if reset_code == user["password_reset_code"]:
        user["password"] = new_password
        show_message("Password reset successful")

        # Send them back to the homepage after a successful reset
        return redirect("/")

    else:
        # Clear the password reset code in the database, so attackers cannot keep guessing it
        user["password_reset_code"] = ""
        show_error("Incorrect code! Unable to reset password")

    return render_template("submit_reset_code.html", username=username)

"""This is the admin dashboard page. The link to this page is only present for the admin user, so nobody will ever find it!"""
@app.route("/admin_dashboard")
def admin():
    # Display a super secret admin page where we can get statistics on our users
    return render_template("admin.html", users=user_database)