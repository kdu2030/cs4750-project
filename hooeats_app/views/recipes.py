from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json

def recipe(request: HttpRequest) -> HttpResponse:
    #if request.COOKIES.get("user"):
    #     user = json.loads(request.COOKIES.get("user"))["username"]
    #     context = get_recipe_data(username=user)
    #else:
    context = get_recipe_data()
    return render(request, "hooeats_app/recipes.html", context=context)

def get_recipe_data(username: str = ""):

    recipe_query = "SELECT * FROM recipes NATURAL JOIN recipe_tags NATURAL JOIN recipe_ingredients WHERE tag = ?;"

    database = HooEatsDatabase(secure=True)
    low_calorie_recipes = database.execute_secure(True, recipe_query, 'low-calorie')
    high_calorie_recipes = database.execute_secure(True, recipe_query, 'high-calorie')
    breakfast_recipes = database.execute_secure(True, recipe_query, 'breakfast')
    lunch_recipes = database.execute_secure(True, recipe_query, 'lunch')
    dinner_recipes = database.execute_secure(True, recipe_query, 'dinner')
    appetizers_recipes = database.execute_secure(True, recipe_query, 'appetizers')
    desserts_recipes = database.execute_secure(True, recipe_query, 'desserts')

    recipe_types = ['Low Calorie','High Calorie','Breakfast','Lunch','Dinner','Appetizers','Dessert']
    recipe_types_tag = ['low-calorie','high-calorie','breakfast','lunch','dinner','appetizers','desserts']

    database.close()

    context = {
        "low_calorie_recipes": low_calorie_recipes,
        "high_calorie_recipes": high_calorie_recipes,
        "breakfast_recipes": breakfast_recipes,
        "lunch_recipes": lunch_recipes,
        "dinner_recipes": dinner_recipes,
        "appetizers_recipes": appetizers_recipes,
        "desserts_recipes": desserts_recipes,
        "recipe_types": recipe_types,
        "recipe_types_tag": recipe_types_tag
    }

    return context