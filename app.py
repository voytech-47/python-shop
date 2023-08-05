import hashlib
from flask import Flask, render_template, request, Response, redirect, make_response
import mysql.connector
from collections import Counter

app = Flask(__name__, template_folder="./views")


@app.route('/')
def index():
    user_login = request.cookies.get("login")
    try:
        host = "localhost"
        user = "root"
        password = ""
        database = "sklep"
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        response = make_response(
            render_template(template_name_or_list='main/index.html', login=user_login, items=items))
        return response
    except:
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


@app.route("/login")
def login():
    note = ""
    try:
        note = request.cookies.get("note")
    except:
        pass
    return render_template("main/login.html", note=note)


@app.route("/sign-up")
def sign_up():
    return render_template("main/sign_up.html")


@app.route("/api/search_login", methods=["POST"])
def login_api():
    try:
        host = "localhost"
        user = "root"
        password = ""
        database = "sklep"
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connect.cursor()
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
        response = redirect("/")
        response.set_cookie("login", user_login)
        response.set_cookie("note", "", expires=0)
        return response
    except:
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


@app.route("/api/sign_up", methods=["POST"])
def signup_api():
    login = request.form.get("login")
    password = request.form.get("password")
    hashing = hashlib.sha3_256()
    hashing.update(password.encode("utf8"))
    hashed_password = hashing.hexdigest()
    try:
        host = "localhost"
        user = "root"
        password = ""
        database = "sklep"
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connect.cursor()
        query = f"INSERT INTO users VALUES ('', '{login}', '{hashed_password}');"
        cursor.execute(query)
        connect.commit()
        connect.close()
        resp = redirect("/")
        resp.set_cookie("login", login)
        return resp
    except:
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


@app.route("/api/is_login_available", methods=["POST"])
def is_login_available():
    try:
        host = "localhost"
        user = "root"
        password = ""
        database = "sklep"
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connect.cursor()
        cursor.execute("SELECT login, password FROM users")
        users = cursor.fetchall()
        logins = [login for login, _ in users]
        user_login = request.get_json()
        if user_login["login"] in logins:
            return Response(status=418)

        return Response(status=200)
    except:
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


@app.route("/log-out")
def log_out():
    response = redirect("/login")
    response.delete_cookie("login")
    return response


@app.route("/cart")
def cart():
    user_login = request.cookies.get("login")
    cart_value = request.cookies.get("cart_value")
    if cart_value is None:
        cart_value = 0.0
    cart_contents = request.cookies.get("cart_contents")
    if cart_contents is None:
        cart_contents = ""
    else:
        cart_contents = cart_contents.split("_")[:-1]
    cart_dict = dict(Counter(cart_contents))
    try:
        host = "localhost"
        user = "root"
        password = ""
        database = "sklep"
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        for item_id, num_occurrences in cart_dict.items():
            str_item_id = str(item_id)
            matching_items = [item for item in items if str(item[0]) == str_item_id]
            for matching_item in matching_items:
                item_list = list(matching_item)
                item_list.append(num_occurrences)
                items[items.index(matching_item)] = tuple(item_list)
        resp = make_response(render_template("main/cart.html", login=user_login, cart=items, sum=cart_value))
        return resp
    except:
        return Response(
            response=f"Cannot connect to database is server running? are the credentials correct? is database created?",
            status=500)


def failed_login():
    response = redirect("/login")
    response.set_cookie("note", "Login lub hasło są niepoprawne")
    return response


if __name__ == '__main__':
    app.run()

# tooltip dodano do koszyka
# usuwanie z koszyka
# dynamiczna zmiana ilości przedmiotów
#
