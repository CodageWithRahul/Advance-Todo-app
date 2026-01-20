function togglePassword() {
    const passwordField = document.querySelector('input[type="password"], input[type="text"][name="password"]');

    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}