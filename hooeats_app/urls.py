from django.shortcuts import redirect
from django.urls import path
from .views import views
from .views import auth, dining_halls, meal_planner

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
    path("meal-planner/", meal_planner.meal_planner, name="meal_planner"),
    path("create-meal-plan/", meal_planner.create_meal_plan, name="create_meal_plan"),
    path("update-meal-plan/", meal_planner.update_meal_plan, name="update_meal_plan"),
    path("delete-meal-plan", meal_planner.delete_meal_plan, name="delete_meal_plan"),
    path("api/signup-valid/", auth.signup_valid, name="signup_valid"),
    path("api/dining-hall/<str:title>/<str:dining_hall>/<str:section>/", dining_halls.fetch_nutritional_data, name="meal_nutrition"),
    path("api/dining-hall/insert-bookmark/", dining_halls.insert_bookmark, name="insert_bookmark"),
    path("api/dining-hall/remove-bookmark/", dining_halls.remove_bookmark, name="remove_bookmark"),
    path("api/meal-planner/insert-uva-meal/", meal_planner.insert_uva_meal, name="insert_uva_meal"),
    path("api/meal-planner/update-uva-meal/", meal_planner.update_uva_meal, name="update_uva_meal"),
    path("api/meal-planner/delete-uva-meal/", meal_planner.delete_uva_meal, name="delete_uva_meal")
]