const carouselPositions = new Map();

const initializeCarousel = () => {
    const tags = ['low-calorie','breakfast','lunch','dinner','appetizers','desserts','vegetarian','vegan'];
    //const tags = ['low-calorie'];
    // carouselWidth = $(".carousel-inner")[0].scrollWidth;
    // cardWidth = $(".carousel-item").width();
    // scrollPosition = 0;
    tags.forEach((tag) => {
        const carouselTagData = {
            carouselWidth: $(`#${tag}-controls .carousel-inner`)[0].scrollWidth,
            cardWidth: $(`#${tag}-controls .carousel-item`).width(),
            scrollPosition: 0
        };
        carouselPositions.set(tag, carouselTagData);
    })

}

window.addEventListener("load", initializeCarousel);

const nextButton = (tag) => {
    // if (scrollPosition < carouselWidth - cardWidth * 4) {
    //     scrollPosition += cardWidth;
    //     $("#lowCalorieControls .carousel-inner").animate(
    //         { scrollLeft: scrollPosition },
    //         600
    //     );
    // }
    const carouselData = carouselPositions.get(tag);
    let scrollPosition = carouselData.scrollPosition;
    let carouselWidth = carouselData.carouselWidth;
    let cardWidth = carouselData.cardWidth;
    
    if (scrollPosition < carouselWidth - cardWidth * 4) {
        scrollPosition += cardWidth;
        $(`#${tag}-controls .carousel-inner`).animate(
            { scrollLeft: scrollPosition },
            600
        );
    }

    const newCarouselData = {
        scrollPosition,
        carouselWidth,
        cardWidth,
    };

    carouselPositions.set(tag, newCarouselData);

}

const prevButton = (tag) => {
    const carouselData = carouselPositions.get(tag);
    let scrollPosition = carouselData.scrollPosition;
    let carouselWidth = carouselData.carouselWidth;
    let cardWidth = carouselData.cardWidth;

    if (scrollPosition > 0) {
        scrollPosition -= cardWidth;
        $(`#${tag}-controls .carousel-inner`).animate(
          { scrollLeft: scrollPosition },
          600
        );
    }

    const newCarouselData = {
        scrollPosition,
        carouselWidth,
        cardWidth,
    };

    carouselPositions.set(tag, newCarouselData);
}





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
    fetch(`/api/dining-hall/${title}/${diningHall}/${section}`)
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
                if (key === "description") {
                    continue;
                }
                else if (["cholesterol", "sodium"].includes(key)) {
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
const toggleAddRemove = (recipeId, showAdd) => {
    const addButton = document.getElementById(`add-bookmark-${recipeId}`);
    console.log(addButton);
    const removeButton = document.getElementById(`remove-bookmark-${recipeId}`);
    console.log(removeButton);
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
const addBookmark = (recipeId, recipeName) => {
    const data = {
        recipe_id: recipeId
    };

    const words = recipeName.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }

    postToRecipesAPI("/api/recipes/insert-bookmark/", data)
        .then((response) => {
            if (response.result === "Insertion Successful") {
                const header = `<i class="bi bi-bookmark-check me-3"></i> Successfully Bookmarked Meal`;
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
const removeBookmark = (recipeId, recipeName) => {
    const data = {
        recipe_id: recipeId
    };

    const words = recipeName.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }

    postToRecipesAPI("/api/recipes/remove-bookmark/", data)
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
