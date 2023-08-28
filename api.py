import hashlib

from flask import session, redirect, Response, request, url_for

from app import app
from model import log_in, sign_up, get_users, delete_item_by_id, update_item_info, add_item_to_db, get_price_by_id


@app.route("/api/search_login", methods=["POST"])
def login_api():
    user_login = request.form.get("login")
    user_password = request.form.get("password")
    log_in(user_login, user_password)
    session.modified = True
    return redirect("/")


@app.route("/api/sign_up", methods=["POST"])
def signup_api():
    user_login = request.form.get("login")
    password = request.form.get("password")
    hashing = hashlib.sha3_256()
    hashing.update(password.encode("utf8"))
    hashed_password = hashing.hexdigest()
    sign_up(user_login, hashed_password)
    session.modified = True
    return redirect("/")


@app.route("/api/is_login_available", methods=["POST"])
def is_login_available():
    users = get_users()
    logins = [user_login for user_login, _ in users]
    user_login = request.get_json()
    if user_login["login"] in logins:
        return Response(status=418)

    return Response(status=200)


@app.route("/api/delete_item/<int:id>")
def delete_item(id):
    delete_item_by_id(id)
    resp = redirect("/admin")
    return resp


@app.route("/api/change_item_info", methods=["POST"])
def change_item_info():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    price = float(request.form.get("price"))
    photo = request.form.get("photo")
    update_item_info(name, price, photo, id)
    resp = redirect("/admin")
    return resp


@app.route("/api/add_item", methods=["POST"])
def add_item():
    name = request.form.get("name")
    price = float(request.form.get("price"))
    photo = request.form.get("photo")
    add_item_to_db(name, price, photo)
    resp = redirect("/admin")
    return resp


@app.route("/api/add_to_cart/<int:id>")
def add_to_cart(id):
    if str(id) in session["cart"]["contents"]:
        session["cart"]["contents"][str(id)] += 1
    else:
        session["cart"]["contents"][str(id)] = 1
    price = get_price_by_id(id)
    session["cart"]["value"] += price
    session["cart"]["quantity"] += 1
    session.modified = True
    return redirect(url_for("index", last_changed=id))


@app.route('/api/delete_from_cart/<int:id>')
def delete_from_cart(id):
    amount = session["cart"]["contents"][str(id)]
    session["cart"]["contents"].pop(str(id))
    session["cart"]["quantity"] -= amount
    price = get_price_by_id(id)
    session["cart"]["value"] -= amount * price
    session.modified = True
    return redirect("/cart")


@app.route('/api/add_amount/<int:id>')
def add_amount(id):
    session["cart"]["contents"][str(id)] += 1
    session["cart"]["quantity"] += 1
    price = get_price_by_id(id)
    session["cart"]["value"] += price
    session.modified = True
    return redirect("/cart")


@app.route('/api/remove_amount/<int:id>')
def remove_amount(id):
    session["cart"]["contents"][str(id)] -= 1
    session["cart"]["quantity"] -= 1
    price = get_price_by_id(id)
    session["cart"]["value"] -= price
    session.modified = True
    return redirect("/cart")


@app.route("/api/change_amount/<int:id>/<int:amount>")
def change_amount(id, amount):
    old_amount = session["cart"]["contents"][str(id)]
    session["cart"]["contents"][str(id)] = amount
    session["cart"]["quantity"] -= old_amount
    session["cart"]["quantity"] += amount
    price = get_price_by_id(id)
    session["cart"]["value"] -= old_amount * price
    session["cart"]["value"] += amount * price
    session.modified = True
    return redirect("/cart")
