import secrets
from flask import Flask, render_template, request, redirect, make_response, session
import model

app = Flask(__name__, template_folder="./views")
app.secret_key = secrets.token_hex()


@app.route('/')
def index(file="index.html"):
    last_changed = request.args.get("last_changed")
    if last_changed is not None:
        last_changed = int(last_changed)
    if "login" not in session or (session["login"] != "admin" and file == "admin.html"):
        return redirect("/login")
    user_login = session["login"]
    items = model.get_all_items()
    template_file = f'main/{file}'
    response = make_response(
        render_template(template_name_or_list=template_file, login=user_login, items=items,
                        last_changed=last_changed))
    return response


@app.route('/api/sign_up', methods=["POST"])
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
    model.save_cart_to_db(user_login)
    session.clear()
    return redirect("/login")


@app.route("/cart")
def cart():
    user_login = session["login"]
    cart_info = session["cart"]
    cart_contents = model.get_items_for_cart(cart_info)
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

#
# if __name__ == '__main__':
#     app.run()
