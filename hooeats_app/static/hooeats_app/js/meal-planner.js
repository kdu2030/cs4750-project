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

const getBookmarkedMeals = () => {
    const bookmarkedMealsElement = document.getElementById("bookmarked-meals-data");
    const mealsData = JSON.parse(bookmarkedMealsElement.innerText)
    const mealsMap = new Map();
    mealsData.forEach((meal) => {
        mealsMap.set(meal.meal_id, meal);
    })
    return mealsMap;
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
    const bookmarkedMeals = getBookmarkedMeals();
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
    if(targetClasses.includes("meal-card")){
        return false;
    } else if(targetClasses.includes("meal-plan-cell") && elementClasses.includes("uva-dining-meal")){
        return checkMealDate(element, target);
    }
    return true;
}

const showMealData = (mealId) => {
    const bookmarkedMeals = getBookmarkedMeals();
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
    const bookmarkedMeals = getBookmarkedMeals();
    const mealId = Number.parseInt(mealElement.getAttribute("data-meal-id"));
    const mealData = bookmarkedMeals.get(mealId);
    const mealType = target.getAttribute("data-meal-type");
    const mealPlanData = getMealPlanData()
    const planId = mealPlanData.plan_id;
    let offset = Number.parseInt(target.getAttribute("data-date")) - 1;
    if(offset < 0){
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
        if(response["result"] === "Insertion successful"){
            const header = `<i class="bi bi-file-earmark-plus me-3"></i> Added Meal to Meal Plan`;
            const message = `Added ${mealData.title} to ${mealPlanData.plan_name}`;
            addToast(header, message, true);
        }
        else{
            const header = `<i class="bi bi-file-earmark-excel me-3"></i> Unable to Add Meal to Meal Plan`;
            const message = `Unable to add ${mealData.title} to ${mealPlanData.plan_name}`;
            addToast(header, message, false);
        }
    })
       
}

const handleDrop = (element, target, source) => {
    const sourceClasses = [...source.classList]
    const targetClasses = [...target.classList];
    const elementClasses = [...element.classList];

    // A UVA Dining Meal Card is moving from the accordion to the Meal Plan Table
    if(sourceClasses.includes("meal-card") && targetClasses.includes("meal-plan-cell") && elementClasses.includes("uva-dining-meal")){
        addMealItem(element, target);
    }
}

const initDragAndDrop = () => {
    const dragAndDrop = dragula([...document.getElementsByClassName("meal-card"), ...document.getElementsByClassName("meal-plan-cell")], {
        copy: (element, source) => checkCopy(element, source),
        accepts: (element, target, source, sibling) => checkAcceptDrop(element, target, source, sibling),
        revertOnSpill: false,
        removeOnSpill: true
    })
    dragAndDrop.on("drop", handleDrop);
}

window.addEventListener("load", initDragAndDrop);