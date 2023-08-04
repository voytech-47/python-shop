import hashlib

from flask import Flask, render_template, request, Response, redirect, make_response
import mysql.connector

app = Flask(__name__, template_folder="./views")


@app.route('/')
def index():
    user_login = request.cookies.get("login")
    response = make_response(render_template(template_name_or_list='main/index.html', login=user_login))
    return response


@app.route("/login")
def login():
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
        logins = [login for login, _ in users]
        user_login = request.form.get("login")
        if user_login not in logins:
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
def is_login_abailable():
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


def failed_login():
    response = redirect("/login")
    response.set_cookie("note", "Login lub hasło są niepoprawne")
    return response


if __name__ == '__main__':
    app.run()
