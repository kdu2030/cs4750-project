from django.shortcuts import redirect
from django.urls import path
from .views import views
from .views import auth, dining_halls, meal_planner, dashboard, recipes, account_settings, search_results

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", auth.signup, name="signup"),
    path("signin/", auth.signin, name="signin"),
    path("signout/", auth.signout, name="signout"),
    path("signin/<str:error>/", auth.signin_error, name="signin_error"),
    path("signup/<str:error>/", auth.signup_error, name="signup_error"),
    path("dining-hall/<str:dining_hall>/", dining_halls.dining_hall, name="dining_hall"),
    path("dining-hall/<str:dining_hall>/<str:date_str>/", dining_halls.dining_hall_date, name="dining_hall_date"),
    path("dining-hall/<str:dining_hall>/<str:date_str>/<str:meal_type>/", dining_halls.dining_hall_meal, name="dining_hall_meal"),
    path("handle-signin/", auth.handle_signin, name="handle_signin"),
    path("handle-signup/", auth.handle_signup, name="handle_signup"),
    path("meal-planner/<int:plan_id>/", meal_planner.meal_plan_specific, name="specific_meal_plan"),
    path("meal-planner/", meal_planner.meal_planner, name="meal_planner"),
    path("create-meal-plan/", meal_planner.create_meal_plan, name="create_meal_plan"),
    path("update-meal-plan/", meal_planner.update_meal_plan, name="update_meal_plan"),
    path("delete-meal-plan", meal_planner.delete_meal_plan, name="delete_meal_plan"),
    path("dashboard/", dashboard.dashboard, name="dashboard"),
    path("account-settings/update-account/", account_settings.update_account, name="update_account"),
    path("account-settings/update-password/", account_settings.change_password, name="update_password"),
    path("account-settings/<str:message>/", account_settings.account_settings, name="account_settings"),
    path("account-settings/", account_settings.account_settings, name="account_settings"),
    path("search/", search_results.search_results_view, name="search_results"),
    path("api/signup-valid", auth.signup_valid, name="signup_valid"),
    path("api/dining-hall/<str:title>/<str:dining_hall>/<str:section>/", dining_halls.fetch_nutritional_data, name="meal_nutrition"),
    path("api/search-results/<str:recipe_id>/", search_results.fetch_recipe_nutritional_data, name="recipe_nutrition"),
    path("api/dining-hall/insert-bookmark/", dining_halls.insert_bookmark, name="insert_bookmark"),
    path("api/dining-hall/remove-bookmark/", dining_halls.remove_bookmark, name="remove_bookmark"),
    path("api/recipes/insert-bookmark/", recipes.insert_bookmark, name="insert_bookmark"),
    path("api/recipes/remove-bookmark/", recipes.remove_bookmark, name="remove_bookmark"),
    path("api/recipes/<str:recipe_id>/", recipes.fetch_recipe_nutritional_data, name="recipe_nutrition"),
    path("recipes", recipes.recipe, name="recipes"),
    path("api/meal-planner/insert-uva-meal/", meal_planner.insert_uva_meal, name="insert_uva_meal"),
    path("api/meal-planner/update-uva-meal/", meal_planner.update_uva_meal, name="update_uva_meal"),
    path("api/meal-planner/delete-uva-meal/", meal_planner.delete_uva_meal, name="delete_uva_meal"),
    path("api/meal-planner/insert-recipe/", meal_planner.insert_recipe, name="insert_recipe"),
    path("api/meal-planner/update-recipe/", meal_planner.update_recipe, name="update_recipe"),
    path("api/meal-planner/delete-recipe/", meal_planner.delete_recipe, name="delete_recipe"),
    path("api/recipes/remove-bookmark/", recipes.remove_bookmark, name="recipe_remove_bookmark")
]