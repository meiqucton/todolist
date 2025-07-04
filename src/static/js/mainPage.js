        document.getElementById("Home").addEventListener("click", function () {
            document.getElementById("home").scrollIntoView({ behavior: "smooth" });
        });

        document.getElementById("About").addEventListener("click", function () {
            document.getElementById("about").scrollIntoView({ behavior: "smooth" });
        });

        document.getElementById("singer").addEventListener("click", function () {
            document.getElementById("personal").scrollIntoView({ behavior: "smooth" });
        });

        document.getElementById("Team").addEventListener("click", function () {
            document.getElementById("team").scrollIntoView({ behavior: "smooth" });
        });

        document.getElementById("Contact").addEventListener("click", function () {
            document.getElementById("contact").scrollIntoView({ behavior: "smooth" });
        });
function showLogin() {
  document.getElementById("login-modal").style.display = "flex";
  showLoginForm(); // mặc định hiển thị login
}

function hideLogin() {
  document.getElementById("login-modal").style.display = "none";
}

function showLoginForm() {
  document.getElementById("form-login").style.display = "block";
  document.getElementById("form-register").style.display = "none";

  document.getElementById("btn-login").classList.add("active");
  document.getElementById("btn-register").classList.remove("active");
}

function showRegisterForm() {
  document.getElementById("form-login").style.display = "none";
  document.getElementById("form-register").style.display = "block";

  document.getElementById("btn-login").classList.remove("active");
  document.getElementById("btn-register").classList.add("active");
}

