import secrets

import mysql.connector
from flask import Flask, render_template, request, redirect, make_response

from model import *

app = Flask(__name__, template_folder="./views")
app.secret_key = secrets.token_hex()


def db_connect():
    host = "localhost"
    user = "root"
    password = ""
    database = "sklep"
    connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = connect.cursor()
    return connect, cursor


@app.route('/')
def index(file="index.html"):
    last_changed = request.args.get("last_changed")
    if last_changed is not None:
        last_changed = int(last_changed)
    if "login" not in session or (session["login"] != "admin" and file == "admin.html"):
        return redirect("/login")
    user_login = session["login"]
    items = get_all_items()
    template_file = f'main/{file}'
    response = make_response(
        render_template(template_name_or_list=template_file, login=user_login, items=items,
                        last_changed=last_changed))
    return response


@app.route("/login")
def login():
    note = ""
    try:
        note = session["note"]
    except:
        pass
    return render_template("main/login.html", note=note)


@app.route("/sign-up")
def sign_up():
    return render_template("main/sign_up.html")


@app.route("/log_out")
def log_out():
    user_login = session["login"]
    save_cart_to_db(user_login)
    session.clear()
    return redirect("/login")


@app.route("/cart")
def cart():
    user_login = session["login"]
    cart_info = session["cart"]
    cart_contents = get_items_for_cart(cart_info)
    resp = make_response(
        render_template("main/cart.html", login=user_login, cart=cart_contents, sum=cart_info["value"]))
    return resp


@app.route("/admin")
def admin_panel():
    response = index("admin.html")
    return response


@app.route("/admin/new_item")
def new_item():
    user_login = session["login"]
    cart_value = session["cart"]["value"]
    return render_template("main/new_item.html", login=user_login, sum=cart_value)


def failed_login():
    session["note"] = "Login lub hasło są niepoprawne"
    return redirect("/login")


if __name__ == '__main__':
    app.run()
