var checkConfirmPassword = function () {
    var signupForm = document.getElementById("signup-form");
    var passwordField = document.querySelector("input[name='password']");
    var confirmPasswordField = document.querySelector("input[name='confirm_password']");
    if (!signupForm || !passwordField || !confirmPasswordField) {
        return;
    }
    if (passwordField.value !== confirmPasswordField.value) {
        confirmPasswordField.setCustomValidity("Passwords do not match");
        confirmPasswordField.reportValidity();
    }
    else {
        confirmPasswordField.setCustomValidity("");
        signupForm.submit();
    }
};
