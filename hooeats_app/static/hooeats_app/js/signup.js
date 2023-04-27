var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const addToastToPage = (header, message, successful) => {
    var _a;
    //Get template for the toast
    const toast = (_a = document.getElementById("success-toast")) === null || _a === void 0 ? void 0 : _a.cloneNode(true);
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
    setTimeout(() => { toastContainer.removeChild(toast); }, 5000);
};
const postToApi = (url, data) => __awaiter(this, void 0, void 0, function* () {
    const token = document.getElementsByName("csrfmiddlewaretoken")[0];
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
    };
    try {
        const response = yield fetch(url, request);
        return yield response.json();
    }
    catch (error) {
        return { "result": "Connection Failure" };
    }
});
const checkUnique = () => __awaiter(this, void 0, void 0, function* () {
    const emailField = document.querySelector("input[name='email']");
    const usernameField = document.querySelector("input[name='username']");
    if (!emailField || !usernameField) {
        return false;
    }
    const userData = {
        "email": emailField.value,
        "username": usernameField.value
    };
    const response = yield postToApi("/api/signup-valid/", userData);
    switch (response["result"]) {
        case "Signup Valid":
            emailField.setCustomValidity("");
            usernameField.setCustomValidity("");
            return true;
        case "Duplicate Username":
            usernameField.setCustomValidity("A user with this username already exists.");
            usernameField.reportValidity();
            setTimeout(() => usernameField.setCustomValidity(""), 5000);
            return false;
        case "Duplicate Email":
            emailField.setCustomValidity("A user with this email already exists.");
            emailField.reportValidity();
            setTimeout(() => emailField.setCustomValidity(""), 5000);
            return false;
        default:
            const header = `<i class="bi bi-x-circle-fill"></i> Unable to Connect`;
            const message = "We were unable to reach our servers. Please try again.";
            addToastToPage(header, message, false);
            return false;
    }
});
const checkConfirmPassword = () => {
    const passwordField = document.querySelector("input[name='password']");
    const confirmPasswordField = document.querySelector("input[name='confirm_password']");
    if (!passwordField || !confirmPasswordField) {
        return false;
    }
    if (passwordField.value !== confirmPasswordField.value) {
        confirmPasswordField.setCustomValidity("Passwords do not match");
        confirmPasswordField.reportValidity();
        setTimeout(() => confirmPasswordField.setCustomValidity(""), 5000);
        return false;
    }
    confirmPasswordField.setCustomValidity("");
    return true;
};
const checkSignup = () => __awaiter(this, void 0, void 0, function* () {
    const signupForm = document.getElementById("signup-form");
    if (!signupForm) {
        return;
    }
    const passwordValid = checkConfirmPassword();
    if (!passwordValid) {
        return;
    }
    const usernameEmailValid = yield checkUnique();
    if (!usernameEmailValid) {
        return;
    }
    signupForm.submit();
});
