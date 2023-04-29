from traceback import print_exc
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json

def recipe(request: HttpRequest) -> HttpResponse:
    if request.COOKIES.get("user"):
         user = json.loads(request.COOKIES.get("user"))["username"]
         context = get_recipe_data(username=user)
    else:
        context = get_recipe_data()
    return render(request, "hooeats_app/recipes.html", context=context)

def get_info(recipes):
    database = HooEatsDatabase(secure=True)
    for recipe in recipes:
        recipe_tag_query = "SELECT tag FROM recipe_tags WHERE recipe_id = ?;"
        tags = database.execute_secure(True, recipe_tag_query, recipe["recipe_id"])
        recipe["tags"] = []
        for tag in tags:
            recipe["tags"].append(tag['tag'])
    for recipe in recipes:
        recipe_ingredients_query = "SELECT ingredient FROM recipe_ingredients2 WHERE recipe_id = ?;"
        ingredients = database.execute_secure(True, recipe_ingredients_query, recipe["recipe_id"])
        recipe["ingredients"] = []
        for ingredient in ingredients:
            recipe["ingredients"].append(ingredient['ingredient'])
    database.close()
    return recipes

def get_recipe_data(username: str = ""):

    #tags_query = "SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag = ?;"
    recipe_query = "SELECT * FROM (SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag LIKE ?) AS recipe_explorer_tags NATURAL JOIN recipes NATURAL JOIN recipe_images NATURAL JOIN recipe_instructions LIMIT 8;"

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

    context = {
        "low_calorie_recipes": get_info(low_calorie_recipes),
        "breakfast_recipes": get_info(breakfast_recipes),
        "lunch_recipes": get_info(lunch_recipes),
        "dinner_recipes": get_info(dinner_recipes),
        "appetizers_recipes": get_info(appetizers_recipes),
        "desserts_recipes": get_info(desserts_recipes),
        "vegetarian_recipes": get_info(vegetarian_recipes),
        "vegan_recipes": get_info(vegan_recipes),
        "recipe_types": recipe_types,
        "recipe_types_tag": recipe_types_tag
    }

    
    if len(username) > 0:
        bookmarked_recipes = get_bookmarked_recipes(database, username)

        for low_calorie_recipe in low_calorie_recipes:
            if low_calorie_recipe["recipe_id"] in bookmarked_recipes:
                low_calorie_recipe["is_bookmarked"] = True
            else:
                 low_calorie_recipe["is_bookmarked"] = False
        for breakfast_recipe in breakfast_recipes:
            if breakfast_recipe["recipe_id"] in bookmarked_recipes:
                breakfast_recipe["is_bookmarked"] = True
            else:
                 breakfast_recipe["is_bookmarked"] = False
        for lunch_recipe in lunch_recipes:
            if lunch_recipe["recipe_id"] in bookmarked_recipes:
                lunch_recipe["is_bookmarked"] = True
            else:
                 lunch_recipe["is_bookmarked"] = False
        for dinner_recipe in dinner_recipes:
            if dinner_recipe["recipe_id"] in bookmarked_recipes:
                dinner_recipe["is_bookmarked"] = True
            else:
                 dinner_recipe["is_bookmarked"] = False
        for appetizers_recipe in appetizers_recipes:
            if appetizers_recipe["recipe_id"] in bookmarked_recipes:
                appetizers_recipe["is_bookmarked"] = True
            else:
                 appetizers_recipe["is_bookmarked"] = False
        for desserts_recipe in desserts_recipes:
            if desserts_recipe["recipe_id"] in bookmarked_recipes:
                desserts_recipe["is_bookmarked"] = True
            else:
                 desserts_recipe["is_bookmarked"] = False
        for vegetarian_recipe in vegetarian_recipes:
            if vegetarian_recipe["recipe_id"] in bookmarked_recipes:
                vegetarian_recipe["is_bookmarked"] = True
            else:
                 vegetarian_recipe["is_bookmarked"] = False
        for vegan_recipe in vegan_recipes:
            if vegan_recipe["recipe_id"] in bookmarked_recipes:
                vegan_recipe["is_bookmarked"] = True
            else:
                 vegan_recipe["is_bookmarked"] = False

    database.close()

    return context

def get_bookmarked_recipes(database: HooEatsDatabase, username: str) -> List[Dict]:
     query = "SELECT recipe_id FROM bookmark_recipes WHERE username=?"
     recipe_data =  database.execute_secure(True, query, username)
     recipe_ids = []
     for recipe in recipe_data:
          recipe_ids.append(recipe["recipe_id"])
     return recipe_ids

def insert_bookmark(request: HttpRequest) -> JsonResponse:
    if request.COOKIES.get("user") is None:
            return JsonResponse({"result": "Authentication error"})
    data = json.loads(request.body)
    recipe_id = data["recipe_id"]
    username = json.loads(request.COOKIES.get("user"))["username"]
    query = "INSERT INTO bookmark_recipes (username, recipe_id) VALUES (?, ?);"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, query, username, recipe_id)
        database.close()
        return JsonResponse({"result": "Insertion Successful"})
    except:
        print_exc()
        return JsonResponse({"result": "Database Error"})

def remove_bookmark(request: HttpRequest) -> JsonResponse:
    if request.COOKIES.get("user") is None:
            return JsonResponse({"result": "Authentication error"})
    user = json.loads(request.COOKIES.get("user"))["username"]
    data = json.loads(request.body)
    delete_bookmark_query = "DELETE FROM bookmark_recipes WHERE recipe_id = ? AND username=?;"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, delete_bookmark_query, data["recipe_id"], user)
        database.close()
        return JsonResponse({"result": "Deletion Successful"})
    except:
        print_exc()
        return JsonResponse({"result": "Database Error"})
    
def fetch_recipe_nutritional_data(request: HttpRequest, recipe_id: int) -> JsonResponse:
     query = "SELECT * FROM recipes NATURAL JOIN recipe_instructions NATURAL JOIN recipe_images WHERE recipes.recipe_id=?;"
     ingredient_query = "SELECT ingredient FROM recipe_ingredients2 WHERE recipe_id=?;"
     try:
          database = HooEatsDatabase(secure=True)
          nutritional_data = database.execute_secure(True, query, recipe_id)[0]
          ingredient_data = database.execute_secure(True, ingredient_query, recipe_id)
          nutritional_data["ingredients"] = ingredient_data
          nutritional_data["steps"] = eval(nutritional_data["steps"])
          return JsonResponse(nutritional_data)
     except:
          error = {"result": "Database Error"}
          return JsonResponse(error)