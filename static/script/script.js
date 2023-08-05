if (document.cookie.match("note") == null) {
    document.getElementById("note").style.display = "none"
} else {
    document.getElementById("note").style.display = "block"
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
    let item_id = item[0]+"_"
    current_cart_value += item_value
    current_cart_items += item_id
    set_cookie("cart_value", current_cart_value.toFixed(2))
    set_cookie("cart_contents", current_cart_items)
    count_cart()
}

function count_cart() {
    let value = get_cookie("cart_value")
    if (value !== "") {
        document.getElementById("cart_value").innerHTML = value + " zł"
    } else {
        document.getElementById("cart_value").innerHTML = "0.00 zł"
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

function check_amount(field) {
    if (field.value < 1) {
        field.value = 1
    }
}