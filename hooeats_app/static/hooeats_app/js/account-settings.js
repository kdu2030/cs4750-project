const changeProfileImage = (imageUrl) => {
    const profileImage = document.getElementById("profile-image");
    const profileImageField = document.getElementById("profile-image-field");
    if (!profileImage || !profileImageField) {
        return;
    }
    profileImage.setAttribute("src", imageUrl);
    profileImageField.value = imageUrl;
};
const toggleSettings = (showGeneral) => {
    const generalSettingsElement = document.getElementById("general-settings");
    const passwordSettingsElement = document.getElementById("password-settings");
    const generalButton = document.getElementById("general-settings-button");
    const passwordButton = document.getElementById("password-settings-button");
    if (!generalSettingsElement || !passwordSettingsElement || !generalButton || !passwordButton) {
        return;
    }
    if (showGeneral) {
        generalSettingsElement.classList.remove("d-none");
        passwordSettingsElement.classList.add("d-none");
        generalButton.classList.add("list-group-item-success");
        passwordButton.classList.remove("list-group-item-success");
    }
    else {
        generalSettingsElement.classList.add("d-none");
        passwordSettingsElement.classList.remove("d-none");
        passwordButton.classList.add("list-group-item-success");
        generalButton.classList.remove("list-group-item-success");
    }
};
