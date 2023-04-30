var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const addToast = (header, message, successful) => {
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
const addNutritionalInfo = (title, diningHall, section) => {
    // const url = "/api/dining-hall/" + encodeURIComponent(title) + "/" + encodeURIComponent(diningHall) + "/" + encodeURIComponent(section) + "/";
    const url = `/api/dining-hall/${title}/${diningHall}/${section}/`;
    fetch(url)
        .then(response => response.json())
        .then((apiResponse) => {
        // If we get an error from the API
        if ("result" in apiResponse && apiResponse.result === "Database error") {
            const header = `<i class="bi bi-x-circle-fill me-3"></i> Unable to Connect`;
            const message = "We were unable to reach our servers. Please try again.";
            addToast(header, message, false);
            return;
        }
        const modalElements = {
            title: document.getElementById("meal-title"),
            description: document.getElementById("meal-description"),
            serving_size: document.getElementById("serving-size"),
            calories: document.getElementById("calories"),
            calories_from_fat: document.getElementById("calories-from-fat"),
            total_fat: document.getElementById("total-fat"),
            saturated_fat: document.getElementById("saturated-fat"),
            cholesterol: document.getElementById("cholesterol"),
            sodium: document.getElementById("sodium"),
            total_carbohydrates: document.getElementById("total-carbohydrates"),
            protein: document.getElementById("protein"),
            sugar: document.getElementById("sugar"),
            dietary_fiber: document.getElementById("dietary-fiber"),
        };
        const nutritionData = apiResponse;
        if (nutritionData.description) {
            modalElements["description"].innerText = nutritionData.description;
        }
        for (const key in modalElements) {
            if (["cholesterol", "sodium"].includes(key)) {
                modalElements[key].innerText = `${nutritionData[key]} mg`;
            }
            else if (key === "calories") {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
            else if (typeof nutritionData[key] === "number") {
                modalElements[key].innerText = `${nutritionData[key]} g`;
            }
            else {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
        }
    });
};

const populateRecipeIngredients = (ingredientsList) => {
    let ingredientsHTML = "";
    ingredientsList.forEach((ingredient) => {
       ingredientsHTML += `<p class="mb-3">${ingredient.ingredient}</p>` 
    });
    const ingredients = document.getElementById("ingredients");
    ingredients.innerHTML = "";
    ingredients.insertAdjacentHTML("beforeend", ingredientsHTML);
}

const populateRecipeSteps = (recipeList) => {
    let stepsHTML = "";
    recipeList.forEach((recipe, index) => {
        firstLetter = recipe.charAt(0).toUpperCase();
        sentence = firstLetter + recipe.slice(1);
        sentence = sentence.replace("degrees f", "degrees F");
        sentence = sentence.replaceAll(" , ", ", ")
        sentence = sentence.replaceAll(" / ", "/")
        if(sentence.search(/[.?!]$/) == -1){
            sentence += ".";
        }
        stepsHTML += `<p class="mb-3" style="text-align: left;">${index + 1}. ${sentence}</p>` 
    });
    const steps = document.getElementById("steps");
    steps.innerHTML = "";
    steps.insertAdjacentHTML("beforeend", stepsHTML);
}

const addRecipeNutritionalInfo = (recipe_id) => {
    // const url = "/api/search-results/" + encodeURIComponent(recipe_id) + "/";
    const url = `/api/search-results/${recipe_id}/`;
    fetch(url)
        .then(response => response.json())
        .then((apiResponse) => {
        // If we get an error from the API
        if ("result" in apiResponse && apiResponse.result === "Database error") {
            const header = `<i class="bi bi-x-circle-fill me-3"></i> Unable to Connect`;
            const message = "We were unable to reach our servers. Please try again.";
            addToast(header, message, false);
            return;
        }
        const modalElements = {
            recipe_name: document.getElementById("recipe-title"),
            //average_rating: document.getElementById("average-rating"),
            mins: document.getElementById("preparation-time"),
            calories: document.getElementById("recipe-calories"),
            total_fat: document.getElementById("recipe-total-fat"),
            saturated_fat: document.getElementById("recipe-saturated-fat"),
            sodium: document.getElementById("recipe-sodium"),
            carbohydrates: document.getElementById("recipe-carbohydrates"),
            protein: document.getElementById("recipe-protein"),
            sugar: document.getElementById("recipe-sugar"),
            //steps: document.getElementById("steps"),
        };
        const nutritionData = apiResponse;
        populateRecipeIngredients(nutritionData.ingredients);
        populateRecipeSteps(nutritionData.steps)
        //if (nutritionData.steps) {
          //  modalElements["steps"].innerText = nutritionData.steps;
        //}
        for (const key in modalElements) {
            if (["sodium"].includes(key)) {
                modalElements[key].innerText = `${nutritionData[key].toFixed(2)} mg`;
            }
            else if (key === "calories") {
                modalElements[key].innerText = `${nutritionData[key].toFixed(0)}`;
            }
            else if (key === "mins") {
                modalElements[key].innerText = `${nutritionData[key].toFixed(2)} minutes`;
            }
            //else if (key === "average_rating") {
              //  modalElements[key].innerText = `${nutritionData[key]}/5`;
            //}
            else if (typeof nutritionData[key] === "number") {
                modalElements[key].innerText = `${nutritionData[key].toFixed(2)} g`;
            }
            else {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
        }
    });
};

const postToDiningHallAPI = (url, data) => __awaiter(this, void 0, void 0, function* () {
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
const toggleAddRemove = (mealId, showAdd) => {
    const addButton = document.getElementById(`add-bookmark-${mealId}`);
    const removeButton = document.getElementById(`remove-bookmark-${mealId}`);
    if (!addButton || !removeButton) {
        return;
    }
    if (showAdd) {
        addButton.classList.remove("d-none");
        addButton.classList.add("d-block");
        removeButton.classList.remove("d-block");
        removeButton.classList.add("d-none");
    }
    else {
        removeButton.classList.remove("d-none");
        removeButton.classList.add("d-block");
        addButton.classList.remove("d-block");
        addButton.classList.add("d-none");
    }
};
const addBookmark = (mealId, mealTitle) => {
    const data = {
        meal_id: mealId
    };
    postToDiningHallAPI("/api/dining-hall/insert-bookmark/", data)
        .then((response) => {
        if (response.result === "Insertion Successful") {
            const header = `<i class="bi bi-bookmark-check me-3"></i> Successfully Bookmarked Meal`;
            const message = `<p>We successfully added ${mealTitle} to your bookmarks.`;
            addToast(header, message, true);
            toggleAddRemove(mealId, false);
        }
        else {
            const header = `<i class="bi bi-bookmark-check me-3"></i> Unable to Add Bookmark`;
            const message = `<p>We were unable to add ${mealTitle} to your bookmarks. Please try again`;
            addToast(header, message, false);
        }
    });
};
const removeBookmark = (mealId, mealTitle) => {
    const data = {
        meal_id: mealId
    };
    postToDiningHallAPI("/api/dining-hall/remove-bookmark/", data)
        .then((response) => {
        if (response.result === "Deletion Successful") {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Successfully Removed Bookmark`;
            const message = `<p>We successfully removed ${mealTitle} from your bookmarks.`;
            addToast(header, message, true);
            toggleAddRemove(mealId, true);
        }
        else {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Unable to Remove Bookmark`;
            const message = `<p>We were unable to remove ${mealTitle} from your bookmarks. Please try again`;
            addToast(header, message, false);
        }
    });
};

const postToRecipesAPI = (url, data) => __awaiter(this, void 0, void 0, function* () {
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

const addRecipeBookmark = (recipeId, recipeName) => {
    const data = {
        recipe_id: recipeId
    };

    const words = recipeName.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }

    postToRecipesAPI("/api/search-results/insert-bookmark/", data)
        .then((response) => {
            if (response.result === "Insertion Successful") {
                const header = `<i class="bi bi-bookmark-check me-3"></i> Successfully Bookmarked Recipe`;
                const message = `<p>We successfully added ${words.join(" ")} to your bookmarks.`;
                addToast(header, message, true);
                toggleAddRemove(recipeId, false);
            }
            else {
                const header = `<i class="bi bi-bookmark-check me-3"></i> Unable to Add Bookmark`;
                const message = `<p>We were unable to add ${words.join(" ")} to your bookmarks. Please try again`;
                addToast(header, message, false);
            }
        });
};
const removeRecipeBookmark = (recipeId, recipeName) => {
    const data = {
        recipe_id: recipeId
    };

    const words = recipeName.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }

    postToRecipesAPI("/api/search-results/remove-bookmark/", data)
        .then((response) => {
            if (response.result === "Deletion Successful") {
                const header = `<i class="bi bi-bookmark-x me-3"></i> Successfully Removed Bookmark`;
                const message = `<p>We successfully removed ${words.join(" ")} from your bookmarks.`;
                addToast(header, message, true);
                toggleAddRemove(recipeId, true);
            }
            else {
                const header = `<i class="bi bi-bookmark-x me-3"></i> Unable to Remove Bookmark`;
                const message = `<p>We were unable to remove ${words.join(" ")} from your bookmarks. Please try again`;
                addToast(header, message, false);
            }
        });
};