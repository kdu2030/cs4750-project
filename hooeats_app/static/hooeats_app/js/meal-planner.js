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
    return JSON.parse(mealPlanElement);
}

const getDateByOffset = (mealPlanData, offset) => {
    const weekStartDate = new Date(mealPlanData.week_start);
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
    const targetClasses = [...target.classList]
    const elementClasses = [...element.classList]
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

const initDragAndDrop = () => {
    dragula([...document.getElementsByClassName("meal-card"), ...document.getElementsByClassName("meal-plan-cell")], {
        copy: (element, source) => checkCopy(element, source),
        accepts: (element, target, source, sibling) => checkAcceptDrop(element, target, source, sibling),
        revertOnSpill: false,
        removeOnSpill: true
    })
}

window.addEventListener("load", initDragAndDrop);