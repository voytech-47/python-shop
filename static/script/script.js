if (window.location.href.split("/").slice(-1).toString() === "login") {
    if (document.cookie.match("note") == null && document.getElementById("note") != null) {
        document.getElementById("note").style.display = "none"
    } else {
        document.getElementById("note").style.display = "block"
    }
}


function is_login_available(login) {
    let timer;
    if (login === "") {
        document.getElementById("login_not_available").style.display = "none";
        document.getElementById("login_available").style.display = "none"
        return;
    }

    clearTimeout(timer);

    timer = setTimeout(function () {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "http://localhost:5000/api/is_login_available", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            "login": login
        }));
        xhr.onload = function () {
            if (login === "") {
                document.getElementById("login_not_available").style.display = "none";
                document.getElementById("login_available").style.display = "none";
                return;
            }
            if (this.status === 200) {
                login_not_available = document.getElementById("login_not_available").style.display = "none";
                login_available = document.getElementById("login_available");
                login_available.innerHTML = "✔ login <i>" + login + "</i> jest dostępny";
                login_available.style.display = "block";
                document.getElementById("submit").removeAttribute("disabled")
                document.getElementById("submit").classList.remove("not-allowed")
                document.getElementById("submit").classList.add("allowed")
            } else {
                login_available = document.getElementById("login_available").style.display = "none";
                login_not_available = document.getElementById("login_not_available");
                login_not_available.innerHTML = "❌ login <i>" + login + "</i> jest już zajęty";
                login_not_available.style.display = "block";
                document.getElementById("submit").setAttribute("disabled", "yes")
                document.getElementById("submit").classList.remove("allowed")
                document.getElementById("submit").classList.add("not-allowed")
            }
        };
    }, 250)
}

function check_form() {
    let login = document.getElementById("login")
    if (login.value === "") {
        return false
    }
    let password = document.getElementById("password")
    let rpt_password = document.getElementById("rpt_password")
    if (password.value !== rpt_password.value) {
        document.getElementById("passwords_not_identical").style.display = "block"
        password.classList.add("bad")
        rpt_password.classList.add("bad")
        return false
    } else {
        password.classList.remove("not-identical")
        rpt_password.classList.remove("not-identical")
        return true
    }

}

function add_to_cart(raw) {
    let current_cart_value = get_cookie("cart_value")
    if (current_cart_value === "") {
        current_cart_value = 0.0
    } else {
        current_cart_value = parseFloat(current_cart_value)
    }
    let current_cart_items = get_cookie("cart_contents")
    let item = raw.getAttribute("data").slice(1, -1).split(", ")
    let item_value = parseFloat(item[2])
    let item_id = item[0] + "_"
    current_cart_value += item_value
    current_cart_items += item_id
    set_cookie("cart_value", current_cart_value.toFixed(2))
    set_cookie("cart_contents", current_cart_items)
    let tooltip = document.getElementsByClassName("tooltip " + item[0])[0]
    tooltip.classList.add("active");
    setTimeout(() => {
        tooltip.classList.remove("active");
    }, 2000);
    count_cart()
}

function count_cart() {
    let value = get_cookie("cart_value")
    if (value !== "") {
        document.getElementById("cart_value").innerHTML = value + " zł"
    } else {
        document.getElementById("cart_value").innerHTML = "0.00 zł"
    }
    if (get_cookie("cart_contents") !== "" && window.location.href.split("/").slice(-1).toString() === "cart") {
        document.getElementById("cart_empty").style.display = "none"
    }
}

document.addEventListener("DOMContentLoaded", function () {
    count_cart()
});

function get_cookie(name) {
    return ('; ' + document.cookie).split(`; ` + name + `=`).pop().split(';')[0];
}

function set_cookie(name, value) {
    document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=/`;
}

function change_amount(field) {
    if (field.value === 0) {
        field.value = 1
    }
}

function update_amount(field) {
    let price = parseFloat(field.getAttribute("data"))
    let amount = parseInt(field.value)
    let old_amount = parseInt(field.getAttribute("old_value"))
    let id = field.classList[1]
    let cart_value = parseFloat(document.getElementById("sum").getAttribute("data"))
    if (amount < 1 || !Number.isInteger(amount)) {
        field.value = 1
        document.getElementsByClassName("price " + id)[0].innerHTML = price + " zł (1 * " + price + " zł)"
        cart_value -= (old_amount * price).toFixed(2)
        cart_value += price.toFixed(2)
        set_cart(cart_value)
    } else {
        document.getElementsByClassName("price " + id)[0].innerHTML = (price * amount).toFixed(2) + " zł (" + amount + " * " + price + " zł)"
        let substr = (old_amount * price).toFixed(2)
        let add = (amount * price).toFixed(2)
        cart_value -= parseFloat(substr)
        cart_value += parseFloat(add)
        set_cart(cart_value)
        if (amount === 1) {
            document.getElementsByClassName("minus-wrap " + id)[0].classList.add("disabled")
        } else {
            document.getElementsByClassName("minus-wrap " + id)[0].classList.remove("disabled")
        }
    }
    field.setAttribute("old_value", amount)
}

function update_amount_click(field, value) {
    let id = field.classList[1]
    let price = parseFloat(document.getElementsByClassName("amount " + id)[0].getAttribute("data"))
    let input_value = parseInt(document.getElementsByClassName("amount " + id)[0].value)
    if (input_value === 1 && value === -1) {
        return
    } else {
        document.getElementsByClassName("minus-wrap " + id)[0].classList.remove("disabled")
    }
    input_value += parseInt(value)
    document.getElementsByClassName("amount " + field.classList[1])[0].value = input_value
    document.getElementsByClassName("amount " + field.classList[1])[0].setAttribute("old_value", input_value)
    document.getElementsByClassName("price " + id)[0].innerHTML = (price * input_value).toFixed(2) + " zł (" + input_value + " * " + price + " zł)"
    let cart_value = parseFloat(document.getElementById("sum").getAttribute("data"))
    if (value > 0) {
        cart_value += price
    } else {
        cart_value -= price
    }
    set_cookie("cart_value", cart_value.toFixed(2))
    set_cart(cart_value)
    if (input_value === 1) {
        document.getElementsByClassName("minus-wrap " + id)[0].classList.add("disabled")
    }
}

function delete_item_from_cart(field) {
    let cart_value = parseFloat(document.getElementById("sum").getAttribute("data"))
    let id = field.classList[1]
    let item = document.getElementsByClassName("amount " + id)[0]
    let amount = item.value
    let price = item.getAttribute("data")
    let substr = (amount * price).toFixed(2)
    cart_value -= parseFloat(substr)
    set_cart(cart_value)
    set_cookie("cart_value", cart_value.toFixed(2))
    let old_items = get_cookie("cart_contents")
    let new_items = old_items.split(id + "_").join("")
    set_cookie("cart_contents", new_items)
    document.getElementsByClassName("item " + id)[0].remove()
    if (get_cookie("cart_contents") === "") {
        document.getElementById("cart_empty").style.display = "block"
    }

}


function confirm_change(prompt) {
    return confirm(prompt)
}

function set_cart(value) {
    document.getElementById("sum").innerHTML = "Suma: " + value.toFixed(2) + " zł"
    document.getElementById("sum").setAttribute("data", value.toFixed(2))
    document.getElementById("cart_value").innerHTML = value.toFixed(2) + " zł"
}