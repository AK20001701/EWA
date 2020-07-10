function showHidePassword() {
        let passwordField = document.getElementById("password_input")
        let showPassword = document.getElementById("showPassword")
        let hidePassword = document.getElementById("hidePassword")

        if (passwordField.type === "password") {
            passwordField.type = "text"
            showPassword.style.display = "block"
            hidePassword.style.display = "none"

        } else {
            passwordField.type = "password"
            showPassword.style.display = "none"
            hidePassword.style.display = "block"
        }
    }