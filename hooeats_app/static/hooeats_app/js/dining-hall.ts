type APIResponse = {
    result: string,
}

type NutritionElements = {
    [key: string]: HTMLElement,
    title: HTMLElement,
    description: HTMLElement,
    serving_size: HTMLElement,
    calories: HTMLElement,
    calories_from_fat: HTMLElement,
    total_fat: HTMLElement,
    saturated_fat: HTMLElement,
    total_carbohydrates: HTMLElement,
    sodium: HTMLElement,
    sugar: HTMLElement,
    protein: HTMLElement,
    cholesterol: HTMLElement,
    dietary_fiber: HTMLElement, 
  }

type NutritionData = {
    [key: string]: string | number,
    title: string,
    dining_hall: string,
    section: string,
    description: string,
    serving_size: number,
    calories: number,
    calories_from_fat: number,
    total_fat: number,
    saturated_fat: number,
    total_carbohydrates: number,
    sodium: number,
    sugar: number,
    protein: number,
    cholesterol: number,
    dietary_fiber: number
}


type NutritionAPIResponse = NutritionData | APIResponse;

const addToast = (header: string, message: string, successful: boolean) => {
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

const addNutritionalInfo = (title: string, diningHall: string, section: string) => {
    const url = "/api/dining-hall/" + encodeURIComponent(title) + "/" + encodeURIComponent(diningHall) + "/" + encodeURIComponent(section);
    fetch(url)
    .then(response => response.json())
    .then((apiResponse: NutritionAPIResponse) => {
        // If we get an error from the API
        if("result" in apiResponse && apiResponse.result === "Database error"){
            const header = `<i class="bi bi-x-circle-fill me-3"></i> Unable to Connect`;
            const message = "We were unable to reach our servers. Please try again.";
            addToast(header, message, false);
            return;
        }
        
        const modalElements:NutritionElements = {
            title: document.getElementById("meal-title") as HTMLElement,
            description: document.getElementById("meal-description") as HTMLElement,
            serving_size: document.getElementById("serving-size") as HTMLElement,
            calories: document.getElementById("calories") as HTMLElement,
            calories_from_fat: document.getElementById("calories-from-fat") as HTMLElement,
            total_fat: document.getElementById("total-fat") as HTMLElement,
            saturated_fat: document.getElementById("saturated-fat") as HTMLElement,
            cholesterol: document.getElementById("cholesterol") as HTMLElement,
            sodium: document.getElementById("sodium") as HTMLElement,
            total_carbohydrates: document.getElementById("total-carbohydrates") as HTMLElement,
            protein: document.getElementById("protein") as HTMLElement,
            sugar: document.getElementById("sugar") as HTMLElement,
            dietary_fiber: document.getElementById("dietary-fiber") as HTMLElement,
          };
          
        const nutritionData = apiResponse as NutritionData;

        if(nutritionData.description){
            modalElements["description"].innerText = nutritionData.description;
        }

        for(const key in modalElements){
            if(["cholesterol", "sodium"].includes(key)){
                modalElements[key].innerText = `${nutritionData[key]} mg`
            }
            else if(key === "calories"){
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
            else if(typeof nutritionData[key] === "number"){
                modalElements[key].innerText = `${nutritionData[key]} g`
            }
            else {
                modalElements[key].innerText = `${nutritionData[key]}`;
            }
            
        }

    })
}

const postToDiningHallAPI = async (url: string, data: object) => {
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

const toggleAddRemove = (mealId: number, showAdd: boolean) => {
    const addButton = document.getElementById(`add-bookmark-${mealId}`);
    const removeButton = document.getElementById(`remove-bookmark-${mealId}`);
    if(!addButton || !removeButton){
        return;
    }
    if(showAdd){
        addButton.classList.remove("d-none");
        addButton.classList.add("d-block");
        removeButton.classList.remove("d-block");
        removeButton.classList.add("d-none");
    }
    else{
        removeButton.classList.remove("d-none");
        removeButton.classList.add("d-block");
        addButton.classList.remove("d-block");
        addButton.classList.add("d-none");
    }
}

const addBookmark = (mealId: number, mealTitle: string) => {
    const data = {
        meal_id: mealId
    };
    postToDiningHallAPI("/api/dining-hall/insert-bookmark/", data)
    .then((response: APIResponse) => {
        if(response.result === "Insertion Successful"){
            const header = `<i class="bi bi-bookmark-check me-3"></i> Successfully Bookmarked Meal`;
            const message = `<p>We successfully added ${mealTitle} to your bookmarks.`;
            addToast(header, message, true);
            toggleAddRemove(mealId, false);
        }
        else{
            const header = `<i class="bi bi-bookmark-check me-3"></i> Unable to Add Bookmark`;
            const message = `<p>We were unable to add ${mealTitle} to your bookmarks. Please try again`;
            addToast(header, message, false);
        }
        
    })
}

const removeBookmark = (mealId: number, mealTitle: string) => {
    const data = {
        meal_id: mealId
    };
    postToDiningHallAPI("/api/dining-hall/remove-bookmark/", data)
    .then((response: APIResponse) => {
        if(response.result === "Deletion Successful"){
            const header = `<i class="bi bi-bookmark-x me-3"></i> Successfully Removed Bookmark`;
            const message = `<p>We successfully removed ${mealTitle} from your bookmarks.`;
            addToast(header, message, true);
            toggleAddRemove(mealId, true);
        }
        else{
            const header = `<i class="bi bi-bookmark-x me-3"></i> Unable to Remove Bookmark`;
            const message = `<p>We were unable to remove ${mealTitle} from your bookmarks. Please try again`;
            addToast(header, message, false);
        }
        
    })
}