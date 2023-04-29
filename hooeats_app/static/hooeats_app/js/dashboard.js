/// <reference path="./dining-hall.ts" />
const removeMealBookmark = (title, mealId) => {
    const mealBookmark = document.getElementById(`meal-${mealId}`);
    if (!mealBookmark) {
        return;
    }
    const data = {
        meal_id: mealId
    };
    postToDiningHallAPI("/api/dining-hall/remove-bookmark/", data)
        .then((response) => {
        if (response.result === "Deletion Successful") {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Successfully Removed Bookmark`;
            const message = `<p>We successfully removed ${title} from your bookmarks.`;
            mealBookmark.remove();
            addToast(header, message, true);
        }
        else {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Unable to Remove Bookmark`;
            const message = `<p>We were unable to remove ${title} from your bookmarks. Please try again`;
            addToast(header, message, false);
        }
    });
};
const removeRecipeBookmark = (title, recipeId) => {
    const recipeBookmark = document.getElementById(`recipe-${recipeId}`);
    if (!recipeBookmark) {
        return;
    }
    const data = {
        recipe_id: recipeId
    };
    postToDiningHallAPI("/api/recipes/remove-bookmark/", data)
        .then((response) => {
        if (response.result === "Deletion Successful") {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Successfully Removed Bookmark`;
            const message = `<p>We successfully removed ${title} from your bookmarks.`;
            recipeBookmark.remove();
            addToast(header, message, true);
        }
        else {
            const header = `<i class="bi bi-bookmark-x me-3"></i> Unable to Remove Bookmark`;
            const message = `<p>We were unable to remove ${title} from your bookmarks. Please try again`;
            addToast(header, message, false);
        }
    });
};
