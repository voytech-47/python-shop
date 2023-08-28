import hashlib

from flask import session, Response

from app import db_connect, failed_login


def save_cart_to_db(login):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"SELECT id FROM users WHERE login='{login}'")
        user_id = cursor.fetchall()[0][0]
        for key, value in session["cart"]["contents"].items():
            cursor.execute(f"INSERT INTO carts VALUES ('', {int(key)}, {value}, {user_id})")
            connect.commit()
        connect.close()
        return
    except Exception as e:
        print(e)
        return Response(status=500)


def get_items_for_cart(cart):
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        for item_id, num_occurrences in cart["contents"].items():
            str_item_id = str(item_id)
            matching_items = [item for item in items if str(item[0]) == str_item_id]
            for matching_item in matching_items:
                item_list = list(matching_item)
                item_list.append(num_occurrences)
                items[items.index(matching_item)] = tuple(item_list)
        return items
    except Exception:
        raise Exception(
            f"Cannot connect to database is server running? are the credentials correct? is database created?")


def get_all_items():
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return items
    except Exception as e:
        print(e)
        return Response(status=500)


def log_in(user_login, user_password):
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        search_user = filter(lambda x: x[1] == user_login, users)
        search_result = next(search_user, None)
        if search_result is None:
            return failed_login()
        hashing = hashlib.sha3_256()
        hashing.update(user_password.encode("utf8"))
        hashed_user_password = hashing.hexdigest()
        if hashed_user_password != search_result[2]:
            return failed_login()

        session["login"] = user_login
        session["note"] = ""
        user_id = search_result[0]
        cursor.execute(f"SELECT item_id, quantity FROM carts WHERE user_id = {user_id}")
        session["cart"] = {
            "value": 0,
            "quantity": 0,
            "contents": {}
        }
        cart_value = 0
        for item in cursor.fetchall():
            session["cart"]["contents"][str(item[0])] = item[1]
            session["cart"]["quantity"] += item[1]
            temp_cursor = connect.cursor()
            temp_cursor.execute(f"SELECT price FROM items WHERE id = {item[0]}")
            price = temp_cursor.fetchall()[0][0]
            temp_cursor.close()
            cart_value += price * item[1]
        session["cart"]["value"] = cart_value
        cursor.execute(f"DELETE FROM carts WHERE user_id = {user_id}")
        connect.commit()
        connect.close()
    except Exception as e:
        print(e)
        return Response(status=500)


def sign_up(user_login, user_password):
    try:
        connect, cursor = db_connect()
        query = f"INSERT INTO users VALUES ('', '{user_login}', '{user_password}');"
        cursor.execute(query)
        connect.commit()
        connect.close()
        session["login"] = user_login
    except Exception as e:
        print(e)
        return Response(status=500)


def get_users():
    try:
        connect, cursor = db_connect()
        cursor.execute("SELECT login, password FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return Response(status=500)


def delete_item_by_id(id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"DELETE FROM items WHERE id = {id}")
        connect.commit()
        connect.close()
    except Exception as e:
        print(e)
        return Response(status=500)


def update_item_info(name, price, photo, id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"UPDATE items SET name='{name}', price={price}, image='{photo}' WHERE id={id};")
        connect.commit()
        connect.close()
    except Exception as e:
        print(e)
        return Response(status=500)


def add_item_to_db(name, price, photo):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"INSERT INTO items VALUES ('', '{name}', {price}, '{photo}');")
        connect.commit()
        connect.close()
    except Exception as e:
        print(e)
        return Response(status=500)


def get_price_by_id(id):
    try:
        connect, cursor = db_connect()
        cursor.execute(f"SELECT price FROM items WHERE id = {str(id)}")
        return cursor.fetchall()[0][0]
    except Exception as e:
        print(e)
        return Response(status=500)
