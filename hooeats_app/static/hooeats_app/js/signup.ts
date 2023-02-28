
const checkConfirmPassword = () => {
    const signupForm = document.getElementById("signup-form") as HTMLFormElement;
    const passwordField = document.querySelector("input[name='password']") as HTMLInputElement;
    const confirmPasswordField = document.querySelector("input[name='confirm_password']") as HTMLInputElement;
    if(!signupForm || !passwordField || !confirmPasswordField){
        return;
    }
    if(passwordField.value !== confirmPasswordField.value){
        confirmPasswordField.setCustomValidity("Passwords do not match");
        confirmPasswordField.reportValidity();
    }
    else {
        confirmPasswordField.setCustomValidity("");
        signupForm.submit();
    }
}