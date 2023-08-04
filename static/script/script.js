let timer;

function is_login_available(login) {
    if (login === "") {
        document.getElementById("login_not_available").style.display = "none";
        document.getElementById("login_available").style.display = "none";
        document.getElementById("submit").classList.add("not-allowed")
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
                document.getElementById("submit").style.backgroundColor = "grey"
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