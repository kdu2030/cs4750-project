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
    const url = "/api/dining-hall/" + encodeURIComponent(title) + "/" + encodeURIComponent(diningHall) + "/" + encodeURIComponent(section);
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
    const url = "/api/search-results/" + encodeURIComponent(recipe_id) + "/";
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
                modalElements[key].innerText = `${nutritionData[key]}mg`;
            }
            else if (key === "calories") {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
            else if (key === "mins") {
                modalElements[key].innerText = `${nutritionData[key]} minutes`;
            }
            //else if (key === "average_rating") {
              //  modalElements[key].innerText = `${nutritionData[key]}/5`;
            //}
            else if (typeof nutritionData[key] === "number") {
                modalElements[key].innerText = `${nutritionData[key]}g`;
            }
            else {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
        }
    });
};