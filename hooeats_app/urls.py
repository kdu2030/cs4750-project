from django.urls import path
from .views import views
from .views import auth, dining_halls, search_results

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", auth.signup, name="signup"),
    path("signin", auth.signin, name="signin"),
    path("signout", auth.signout, name="signout"),
    path("signin/<str:error>/", auth.signin_error, name="signin_error"),
    path("signup/<str:error>/", auth.signup_error, name="signup_error"),
    path("dining-hall/<str:dining_hall>/", dining_halls.dining_hall, name="dining_hall"),
    path("dining-hall/<str:dining_hall>/<str:date_str>/", dining_halls.dining_hall_date, name="dining_hall_date"),
    path("dining-hall/<str:dining_hall>/<str:date_str>/<str:meal_type>/", dining_halls.dining_hall_meal, name="dining_hall_meal"),
    path("search/", search_results.search_results_view, name="search_results"),
    path("handle-signin", auth.handle_signin, name="handle_signin"),
    path("handle-signup", auth.handle_signup, name="handle_signup"),
    path("api/signup-valid", auth.signup_valid, name="signup_valid"),
    path("api/dining-hall/<str:title>/<str:dining_hall>/<str:section>/", dining_halls.fetch_nutritional_data, name="meal_nutrition"),
    path("api/dining-hall/insert-bookmark/", dining_halls.insert_bookmark, name="insert_bookmark"),
    path("api/dining-hall/remove-bookmark/", dining_halls.remove_bookmark, name="remove_bookmark"),
    path("api/search-results/insert-bookmark/", search_results.insert_bookmark_recipe, name="insert_bookmark_recipe"),
    path("api/search-results/remove-bookmark/", search_results.remove_bookmark_recipe, name="remove_bookmark_recipe"),
    path("api/search-results/<str:recipe_id>/", search_results.fetch_recipe_nutritional_data, name="recipe_nutrition"),
]