
const addToastToPage = (header: string, message: string, successful: boolean) => {
    //Get template for the toast
    const toast = document.getElementById("success-toast")?.cloneNode(true) as HTMLElement;
    const toastContainer = document.getElementById("toast-container");
    if (!toast || !toastContainer) {
        return;
    }
    //Display the toast as block - make it visible
    toast.classList.add("d-block");
    toast.innerHTML = `
    <div class="toast-header">
        <span class="header me-auto ${successful ? "text-success" : "text-danger"}">
            ${header}
        </span>
    </div>
    <div class="toast-body">
        <p>${message}</p>
    </div>`;
    //Add child to toast container
    toastContainer.appendChild(toast);
    //Make toast disappear after 5000 ms
    setTimeout(() => { toastContainer.removeChild(toast) }, 5000);
}


const postToApi = async (url: string, data: object) => {
    const token = document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement;
    if (!token) {
        return;
    }
    let request = {
        method: "POST",
        headers: {
            "X-CSRFToken": token.value,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    try {
        const response = await fetch(url, request);
        return await response.json();
    }
    catch (error) {
        return { "result": "Connection Failure" };
    }

}

const checkUnique = async (): Promise<boolean> => {
    const emailField = document.querySelector("input[name='email']") as HTMLInputElement;
    const usernameField = document.querySelector("input[name='username']") as HTMLInputElement;
    if (!emailField || !usernameField) {
        return false;
    }
    const userData = {
        "email": emailField.value,
        "username": usernameField.value
    }
    const response = await postToApi("/api/signup-valid/", userData)

    switch (response["result"]) {
        case "Signup Valid":
            emailField.setCustomValidity("");
            usernameField.setCustomValidity("");
            return true;
        case "Duplicate Username":
            usernameField.setCustomValidity("A user with this username already exists.");
            usernameField.reportValidity();
            return false;
        case "Duplicate Email":
            emailField.setCustomValidity("A user with this email already exists.");
            emailField.reportValidity();
            return false;
        default:
            const header = `<i class="bi bi-x-circle-fill"></i> Unable to Connect`;
            const message = "We were unable to reach our servers. Please try again.";
            addToastToPage(header, message, false);
            return false;
    }
}

const checkConfirmPassword = () => {
    const passwordField = document.querySelector("input[name='password']") as HTMLInputElement;
    const confirmPasswordField = document.querySelector("input[name='confirm_password']") as HTMLInputElement;
    if (!passwordField || !confirmPasswordField) {
        return false;
    }
    if (passwordField.value !== confirmPasswordField.value) {
        confirmPasswordField.setCustomValidity("Passwords do not match");
        confirmPasswordField.reportValidity();
        return false;
    }
    confirmPasswordField.setCustomValidity("");
    return true;
}

const checkSignup = async () => {
    const signupForm = document.getElementById("signup-form") as HTMLFormElement;
    const confirmPasswordField = document.querySelector("input[name='confirm_password']") as HTMLInputElement;
    const emailField = document.querySelector("input[name='email']") as HTMLInputElement;
    const usernameField = document.querySelector("input[name='username']") as HTMLInputElement;
    
    if (!signupForm || !confirmPasswordField || !emailField || !usernameField) {
        return;
    }

    const passwordValid = checkConfirmPassword();
    if (!passwordValid) {
        confirmPasswordField.setCustomValidity("");
        return;
    }

    
    const usernameEmailValid = await checkUnique();
    if (!usernameEmailValid) {
        usernameField.setCustomValidity("");
        return;
    }

    signupForm.submit();
}

