const postToApi = async (url, data) => {
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
    }
    try {
        const response = await fetch(url, request);
        return await response.json();
    }
    catch (error) {
        return { "result": "Connection Failure" };
    }

}

const addToast = (header, message, successful) => {
    //Get template for the toast
    const toast = document.getElementById("success-toast")?.cloneNode(true);
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

const getMealData = () => {
    const mealDataElement = document.getElementById("bookmarked-meals-data");
    const mealsData = JSON.parse(mealDataElement.innerText)
    const mealsMap = new Map();
    mealsData.forEach((meal) => {
        mealsMap.set(meal.meal_id, meal);
    })
    return mealsMap;
}

const getRecipeData = () => {
    const recipeDataElement = document.getElementById("all-recipes-data");
    const recipesData = JSON.parse(recipeDataElement.innerText);
    const recipesMap = new Map();
    recipesData.forEach((recipe) => {
        recipesMap.set(recipe.recipe_id, recipe);
    })
    return recipesMap;
}


const getMealPlanData = () => {
    const mealPlanElement = document.getElementById("meal-plan-data");
    return JSON.parse(mealPlanElement.innerText);
}

const getDateByOffset = (weekStart, offset) => {
    const weekStartDate = new Date(weekStart);
    const msPerDay = 24 * 60 * 60 * 1000;
    return new Date(weekStartDate.getTime() + (offset * msPerDay));
}

const checkMealDate = (element, target) => {
    const bookmarkedMeals = getMealData();
    const targetDay = Number.parseInt(target.getAttribute("data-date"));
    const mealId = Number.parseInt(element.getAttribute("data-meal-id"));
    const mealDate = new Date(bookmarkedMeals.get(mealId).meal_date);
    return targetDay === mealDate.getDay();
}

const checkCopy = (element, source) => {
    return ![...source.classList].includes("meal-plan-cell");
}

const checkAcceptDrop = (element, target, source, sibling) => {
    const targetClasses = [...target.classList];
    const elementClasses = [...element.classList];
    if (targetClasses.includes("meal-card")) {
        return false;
    } else if (targetClasses.includes("recipe-card")) {
        return false;
    } else if (targetClasses.includes("meal-plan-cell") && elementClasses.includes("uva-dining-meal")) {
        return checkMealDate(element, target);
    }
    return true;
}

const showMealData = (mealId) => {
    const bookmarkedMeals = getMealData();
    const nutritionData = bookmarkedMeals.get(mealId);

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


    if (nutritionData.description) {
        modalElements["description"].innerText = nutritionData.description;
    }

    for (const key in modalElements) {
        if (["cholesterol", "sodium"].includes(key)) {
            modalElements[key].innerText = `${nutritionData[key]} mg`
        }
        else if (key === "calories") {
            modalElements[key].innerText = `${nutritionData[key]}`;
        }
        else if (typeof nutritionData[key] === "number") {
            modalElements[key].innerText = `${nutritionData[key]} g`
        }
        else {
            modalElements[key].innerText = `${nutritionData[key]}`;
        }
    }

}

const addMealItem = (mealElement, target) => {
    const allMealsData = getMealData();
    const mealId = Number.parseInt(mealElement.getAttribute("data-meal-id"));
    const mealData = allMealsData.get(mealId);
    const mealType = target.getAttribute("data-meal-type");
    const mealPlanData = getMealPlanData()
    const planId = mealPlanData.plan_id;
    let offset = Number.parseInt(target.getAttribute("data-date")) - 1;
    if (offset < 0) {
        offset = 6;
    }
    const date = getDateByOffset(mealPlanData.week_start, offset);
    const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, 0)}-${date.getDate()}`
    const data = {
        plan_id: planId,
        meal_id: mealId,
        date: dateStr,
        meal_type: mealType
    };
    postToApi("/api/meal-planner/insert-uva-meal/", data)
        .then((response) => {
            if (response["result"] !== "Database error") {
                mealElement.setAttribute("data-plan-item-id", response["result"]);
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Added Meal to Meal Plan`;
                const message = `Added ${mealData.title} to ${mealPlanData.plan_name}`;
                addToast(header, message, true);
            }
            else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Add Meal to Meal Plan`;
                const message = `Unable to add ${mealData.title} to ${mealPlanData.plan_name}`;
                addToast(header, message, false);
                mealElement.setAttribute("data-fade-out", 1);
                $("div[data-fade-out='1']").fadeOut(800, () => mealElement.remove());
            }
        })

}

const updateMealItem = (mealElement, target) => {
    const allMealsData = getMealData();
    const mealId = Number.parseInt(mealElement.getAttribute("data-meal-id"));
    const mealData = allMealsData.get(mealId);
    const mealItemId = mealElement.getAttribute("data-plan-item-id");
    const mealType = target.getAttribute("data-meal-type");
    const mealPlanData = getMealPlanData();
    let offset = Number.parseInt(target.getAttribute("data-date")) - 1;
    if (offset < 0) {
        offset = 6;
    }
    const date = getDateByOffset(mealPlanData.week_start, offset);
    const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, 0)}-${date.getDate()}`
    const data = {
        date: dateStr,
        plan_meal_type: mealType,
        item_id: mealItemId
    }
    postToApi("/api/meal-planner/update-uva-meal/", data)
        .then((response) => {
            if (response["result"] === "Update successful") {
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Updated Meal Successfully`;
                const message = `Updated ${mealData.title}`;
                addToast(header, message, true);
            }
            else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Update Meal`;
                const message = `Unable to update ${mealData.title}`;
                addToast(header, message, false);
            }
        })
}

const deleteMealItem = (mealElement) => {
    const allMealsData = getMealData();
    const mealId = Number.parseInt(mealElement.getAttribute("data-meal-id"));
    const mealData = allMealsData.get(mealId);
    const mealItemId = mealElement.getAttribute("data-plan-item-id");
    const data = {
        item_id: mealItemId
    };
    postToApi("/api/meal-planner/delete-uva-meal/", data)
        .then((response) => {
            if (response["result"] === "Delete successful") {
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Deleted Meal Successfully`;
                const message = `Deleted ${mealData.title}`;
                addToast(header, message, true);
            }
            else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Delete Meal`;
                const message = `Unable to delete ${mealData.title}`;
                addToast(header, message, false);
            }
        })
}

const toTitleCase = (str) => {
    return str.replace(
        /\w\S*/g,
        function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

const addRecipeItem = (recipeElement, target) => {
    const recipeId = Number.parseInt(recipeElement.getAttribute("data-recipe-id"));
    const allRecipesData = getRecipeData();
    const recipeData = allRecipesData.get(recipeId);
    const planData = getMealPlanData();
    const planId = planData.plan_id;
    const mealType = target.getAttribute("data-meal-type");
    let offset = Number.parseInt(target.getAttribute("data-date")) - 1;
    if (offset < 0) {
        offset = 6;
    }
    const date = getDateByOffset(planData.week_start, offset);
    const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, 0)}-${date.getDate()}`;

    const data = {
        recipe_id: recipeId,
        plan_id: planId,
        meal_type: mealType,
        date: dateStr
    };

    postToApi("/api/meal-planner/insert-recipe/", data)
        .then((response) => {
            if (response["result"] !== "Database error") {
                recipeElement.setAttribute("data-plan-item-id", response["result"]);
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Successfully Added Recipe`;
                const message = `Added ${ toTitleCase(recipeData.recipe_name)} to ${planData.plan_name}`;
                addToast(header, message, true);
            } else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Add Recipe`;
                const message = `Unable to add ${toTitleCase(recipeData.recipe_name)} to ${planData.plan_name}`;
                addToast(header, message, false);
                recipeElement.setAttribute("data-fade-out", 1);
                $("div[data-fade-out='1']").fadeOut(800, () => recipeElement.remove());
            }
        });
}

const updateRecipeItem = (recipeElement, target) => {
    const itemId = Number.parseInt(recipeElement.getAttribute("data-plan-item-id"));
    const recipeId = Number.parseInt(recipeElement.getAttribute("data-recipe-id"));
    const allRecipesData = getRecipeData();
    const recipeData = allRecipesData.get(recipeId);
    const planData = getMealPlanData();
    const mealType = target.getAttribute("data-meal-type");
    let offset = Number.parseInt(target.getAttribute("data-date")) - 1;
    if (offset < 0) {
        offset = 6;
    }
    const date = getDateByOffset(planData.week_start, offset);
    const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, 0)}-${date.getDate()}`;

    const data = {
        item_id: itemId,
        plan_meal_type: mealType,
        date: dateStr
    };

    postToApi("/api/meal-planner/update-recipe/", data)
        .then((response) => {
            if (response.result === "Update successful") {
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Updated Recipe`;
                const message = `Updated ${ toTitleCase(recipeData.recipe_name)}`;
                addToast(header, message, true);
            } else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Update Recipe`;
                const message = `Unable to update ${toTitleCase(recipeData.recipe_name)}`;
                addToast(header, message, false);
            }
        });
}

const deleteRecipeItem = (recipeElement) => {
    const itemId = Number.parseInt(recipeElement.getAttribute("data-plan-item-id"));
    const recipeId = Number.parseInt(recipeElement.getAttribute("data-recipe-id"));
    const allRecipesData = getRecipeData();
    const recipeData = allRecipesData.get(recipeId);

    const data = {
        item_id: itemId,
    };

    postToApi("/api/meal-planner/delete-recipe/", data)
        .then((response) => {
            if (response.result === "Delete successful") {
                const header = `<i class="bi bi-file-earmark-plus me-3"></i> Deleted Recipe`;
                const message = `Deleted ${ toTitleCase(recipeData.recipe_name)}`;
                addToast(header, message, true);
            } else {
                const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Delete Recipe`;
                const message = `Unable to delete ${toTitleCase(recipeData.recipe_name)}`;
                addToast(header, message, false);
            }
        });

}

const handleDrop = (element, target, source) => {
    const sourceClasses = [...source.classList];
    const targetClasses = [...target.classList];
    const elementClasses = [...element.classList];

    // A UVA Dining Meal Card is moving from the accordion to the Meal Plan Table
    if (sourceClasses.includes("meal-card") && targetClasses.includes("meal-plan-cell") && elementClasses.includes("uva-dining-meal")) {
        addMealItem(element, target);
    } else if (sourceClasses.includes("meal-plan-cell") && targetClasses.includes("meal-plan-cell") && elementClasses.includes("uva-dining-meal")) {
        // The user is updating a UVA Dining Hall Meal - different meal time
        updateMealItem(element, target);
    } else if (sourceClasses.includes("recipe-card") && targetClasses.includes("meal-plan-cell") && elementClasses.includes("recipe")) {
        // A recipe is moving from the Recipe Accordion to the Meal Plan Table
        addRecipeItem(element, target);
    } else if (sourceClasses.includes("meal-plan-cell") && targetClasses.includes("meal-plan-cell") && elementClasses.includes("recipe")){
        updateRecipeItem(element, target);
    }
}

const handleRemove = (element) => {
    const elementClasses = [...element.classList];

    // We are trying to delete a UVA Dining Hall Meal
    if (elementClasses.includes("uva-dining-meal")) {
        deleteMealItem(element);
    } else if(elementClasses.includes("recipe")){
        deleteRecipeItem(element);
    }


}

const initDragAndDrop = () => {
    const dragAndDrop = dragula([...document.getElementsByClassName("meal-card"), ...document.getElementsByClassName("meal-plan-cell"), ...document.getElementsByClassName("recipe-card")], {
        copy: (element, source) => checkCopy(element, source),
        accepts: (element, target, source, sibling) => checkAcceptDrop(element, target, source, sibling),
        revertOnSpill: false,
        removeOnSpill: true
    })
    dragAndDrop.on("drop", handleDrop);
    dragAndDrop.on("remove", handleRemove);
}

window.addEventListener("load", initDragAndDrop);