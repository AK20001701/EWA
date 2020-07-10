function showHidePassword() {
    let passwordField = document.getElementById("password_input");
    let passwordFieldConf = document.getElementById("password_input_conf");
    let showPassword = document.getElementById("showPassword");
    let hidePassword = document.getElementById("hidePassword");

    let showPasswordConf = document.getElementById("showPasswordConf");
    let hidePasswordConf = document.getElementById("hidePasswordConf");

    if (passwordField.type === "password" || passwordFieldConf.type === "password") {
        passwordField.type = "text";
        passwordFieldConf.type = "text";
        showPassword.style.display = "block";
        showPasswordConf.style.display = "block";
        hidePassword.style.display = "none";
        hidePasswordConf.style.display = "none";

    } else {
        passwordField.type = "password";
        passwordFieldConf.type = "password";
        showPassword.style.display = "none";
        showPasswordConf.style.display = "none";
        hidePassword.style.display = "block";
        hidePasswordConf.style.display = "block";
    }
}
