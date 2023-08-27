import hashlib
import secrets

from flask import Flask, render_template, request, Response, redirect, make_response, session
import mysql.connector
from collections import Counter

app = Flask(__name__, template_folder="./views")
app.secret_key = secrets.token_hex()
app.debug = True


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
    if "login" not in session or (session["login"] != "admin" and file == "admin.html"):
        return redirect("/login")
    user_login = session["login"]
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        template_file = f'main/{file}'
        if "cart" not in session:
            session["cart"] = {
                "value": 0,
                "quantity": 0,
                "contents": {}
            }
        response = make_response(
            render_template(template_name_or_list=template_file, login=user_login, items=items))
        return response
    except Exception as e:
        print(e)
        return Response(status=500)


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


@app.route("/api/search_login", methods=["POST"])
def login_api():
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT login, password FROM users")
        users = cursor.fetchall()
        user_login = request.form.get("login")
        user_password = request.form.get("password")
        search_user = filter(lambda x: x[0] == user_login, users)
        search_result = next(search_user, None)
        if search_result is None:
            return failed_login()
        hashing = hashlib.sha3_256()
        hashing.update(user_password.encode("utf8"))
        hashed_user_password = hashing.hexdigest()
        if hashed_user_password != search_result[1]:
            return failed_login()

        session["login"] = user_login
        session["note"] = ""
        session.modified = True
        return redirect("/")
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/api/sign_up", methods=["POST"])
def signup_api():
    user_login = request.form.get("login")
    password = request.form.get("password")
    hashing = hashlib.sha3_256()
    hashing.update(password.encode("utf8"))
    hashed_password = hashing.hexdigest()
    try:
        connect, cursor = db_connect()
        query = f"INSERT INTO users VALUES ('', '{user_login}', '{hashed_password}');"
        cursor.execute(query)
        connect.commit()
        connect.close()
        session["login"] = user_login
        session.modified = True
        return redirect("/")
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/api/is_login_available", methods=["POST"])
def is_login_available():
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT login, password FROM users")
        users = cursor.fetchall()
        logins = [user_login for user_login, _ in users]
        user_login = request.get_json()
        if user_login["login"] in logins:
            return Response(status=418)

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/api/delete_item/<int:id>")
def delete_item(id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"DELETE FROM items WHERE id = {id}")
        connect.commit()
        connect.close()
        resp = redirect("/admin")
        return resp
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/api/change_item_info", methods=["POST"])
def change_item_info():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    price = float(request.form.get("price"))
    photo = request.form.get("photo")
    try:
        connect, cursor = db_connect()
        cursor.execute(f"UPDATE items SET name='{name}', price={price}, image='{photo}' WHERE id={id};")
        connect.commit()
        connect.close()
        resp = redirect("/admin")
        return resp
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/api/add_item", methods=["POST"])
def add_item():
    name = request.form.get("name")
    price = float(request.form.get("price"))
    photo = request.form.get("photo")
    try:
        connect, cursor = db_connect()
        cursor.execute(f"INSERT INTO items VALUES ('', '{name}', {price}, '{photo}');")
        connect.commit()
        connect.close()
        resp = redirect("/admin")
        return resp
    except Exception as e:
        print(e)
        return Response(status=500)


@app.route("/log-out")
def log_out():
    response = redirect("/login")
    response.delete_cookie("login")
    return response
    user_login = session["login"]
    try:
        connect, cursor = db_connect()
        for key, value in session["cart"]["contents"].items():
            cursor.execute(f"INSERT INTO carts VALUES ('', {key}, {value}, '{user_login}')")
            connect.commit()
        connect.close()
    except Exception as e:
        print(e)
        return Response(status=500)
    session.clear()
    return redirect("/login")



@app.route("/show")
def show_cart():
    print(session)
    return redirect("/")


@app.route("/cart")
def cart():
    user_login = session["login"]
    cart_info = session["cart"]
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        for item_id, num_occurrences in cart_info["contents"].items():
            str_item_id = str(item_id)
            matching_items = [item for item in items if str(item[0]) == str_item_id]
            for matching_item in matching_items:
                item_list = list(matching_item)
                item_list.append(num_occurrences)
                items[items.index(matching_item)] = tuple(item_list)
        resp = make_response(render_template("main/cart.html", login=user_login, cart=items, sum=cart_info["value"]))
        return resp
    except Exception as err:
        print(err)
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


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

# tooltip dodano/usunieto do koszyka
# usuwanie z koszyka
# dynamiczna zmiana ilości przedmiotów
#
