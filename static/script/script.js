function is_login_available(login) {
    if (login === "") {
        document.getElementById("login_not_available").style.display = "none";
        document.getElementById("login_available").style.display = "none"
        return;
    }

    setTimeout(function () {
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
            let login_not_available;
            let login_available;
            if (this.status === 200) {
                document.getElementById("login_not_available").style.display = "none";
                login_available = document.getElementById("login_available");
                login_available.innerHTML = "✔ login <i>" + login + "</i> jest dostępny";
                login_available.style.display = "block";
                document.getElementById("submit").removeAttribute("disabled")
                document.getElementById("submit").classList.remove("not-allowed")
                document.getElementById("submit").classList.add("allowed")
            } else {
                document.getElementById("login_available").style.display = "none";
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

function chech_if_changed() {
    let url = new URL(window.location.href);
    let last_changed = url.searchParams.get("last_changed")
    let tooltip = document.getElementsByClassName("tooltip " + last_changed)[0]
    tooltip.classList.add("active")
    setTimeout(() => {
        document.getElementsByClassName("active")[0].classList.remove("active");
    }, 2000);

}

document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.remove("preload")
    chech_if_changed()
});

function update_amount(field) {
    let amount = parseInt(field.value);

    if (amount <= 0) {
        field.value = 1;
        update_amount_on_server(field);
        return;
    }

    let id = field.classList[1];
    update_amount_on_server(field, id, amount);
}

function update_amount_on_server(field, id, amount) {
    const url = `/api/change_amount/${id}/${amount}`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "multipart/form-data",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        })
        .then(data => {
            console.log("Response data:", data);
            location.reload();
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}

function confirm_change(prompt) {
    return confirm(prompt)
}
