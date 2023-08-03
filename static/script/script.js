let timer;

function is_login_available(login) {
  if (login === "") {
    document.getElementById("login_not_available").style.display = "none";
    document.getElementById("login_available").style.display = "none";
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
      } else {
        login_available = document.getElementById("login_available").style.display = "none";
        login_not_available = document.getElementById("login_not_available");
        login_not_available.innerHTML = "❌ login <i>" + login + "</i> jest już zajęty";
        login_not_available.style.display = "block";
      }
    };
  }, 250)
}