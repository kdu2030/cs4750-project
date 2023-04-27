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

def get_info(recipes):
    database = HooEatsDatabase(secure=True)
    for recipe in recipes:
        tag_query = "SELECT tag FROM recipe_tags WHERE recipe_id=?"
        ingredients_query = "SELECT ingredient FROM recipe_ingredients WHERE recipe_id=?"
        tag_dicts = database.execute_secure(True, tag_query, recipe["recipe_id"])
        ingredient_dicts = database.execute_secure(True, ingredients_query, recipe["recipe_id"])
        all_query = "SELECT * FROM recipes NATURAL JOIN recipe_images WHERE recipe_id=?"
        full = database.execute_secure(True, all_query, recipe["recipe_id"])
        recipe["tags"] = []
        recipe["ingredients"] = []
        recipe["recipe_name"]=[]
        recipe["average_rating"]=[]
        recipe["rating_count"]=[]
        recipe["img_url"]=[]
        for tag_dict in tag_dicts:
            for tag in tag_dict.values():
                recipe["tags"].append(tag)
        for ingredient_dict in ingredient_dicts:
            for ingredient in ingredient_dict:
                recipe["ingredients"].append(ingredient)
    database.close()
    return recipes

def get_recipe_data(username: str = ""):

    #tags_query = "SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag = ?;"
    recipe_query = "SELECT * FROM (SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag LIKE ?) AS recipe_explorer_tags NATURAL JOIN recipes NATURAL JOIN recipe_images;"

    database = HooEatsDatabase(secure=True)
    low_calorie_recipes = database.execute_secure(True, recipe_query, '%low-calorie%')
    breakfast_recipes = database.execute_secure(True, recipe_query, '%breakfast%')
    lunch_recipes = database.execute_secure(True, recipe_query, '%lunch%')
    dinner_recipes = database.execute_secure(True, recipe_query, '%dinner%')
    appetizers_recipes = database.execute_secure(True, recipe_query, '%appetizers%')
    desserts_recipes = database.execute_secure(True, recipe_query, '%desserts%')
    vegetarian_recipes = database.execute_secure(True, recipe_query, '%vegetarian%')
    vegan_recipes = database.execute_secure(True, recipe_query, '%vegan%')

    recipe_types = ['Low Calorie','Breakfast','Lunch','Dinner','Appetizers','Dessert','Vegetarian','Vegan']
    recipe_types_tag = ['low-calorie','breakfast','lunch','dinner','appetizers','desserts','vegetarian','vegan']

    database.close()

    context = {
        "low_calorie_recipes": low_calorie_recipes,
        "breakfast_recipes": breakfast_recipes,
        "lunch_recipes": lunch_recipes,
        "dinner_recipes": dinner_recipes,
        "appetizers_recipes": appetizers_recipes,
        "desserts_recipes": desserts_recipes,
        "vegetarian_recipes": vegetarian_recipes,
        "vegan_recipes": vegan_recipes,
        "recipe_types": recipe_types,
        "recipe_types_tag": recipe_types_tag
    }

    return context