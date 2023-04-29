from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json
from traceback import print_exc

def get_search_results(keyword: str, username: str = ""):
    query_keyword = "%" + keyword + "%"
    uva_dining_search_query = "SELECT * FROM uva_meals NATURAL JOIN uva_descriptions WHERE uva_meals.title LIKE ? OR uva_meals.section LIKE ? OR uva_descriptions.description LIKE ? OR uva_meals.dining_hall LIKE ? LIMIT 10;"
    recipe_search_query = "SELECT * FROM recipes NATURAL JOIN recipe_instructions NATURAL JOIN recipe_images WHERE recipes.recipe_name LIKE ? OR recipe_instructions.steps LIKE ?;"
    recipe_tag_search_query = "SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag LIKE ?;"
    recipe_ingredients_search_query = "SELECT DISTINCT recipe_id FROM recipe_ingredients2 WHERE ingredient LIKE ?;"

    database = HooEatsDatabase(secure=True)
    uva_dining_search_results = database.execute_secure(True, uva_dining_search_query, query_keyword, query_keyword, query_keyword, query_keyword)
    recipe_search_results = database.execute_secure(True, recipe_search_query, query_keyword, query_keyword)
    recipe_tag_search_results = database.execute_secure(True, recipe_tag_search_query, query_keyword)
    recipe_ingredients_search_results = database.execute_secure(True, recipe_ingredients_search_query, query_keyword)

    uva_dining_items = []
    recipe_items = []
    recipes_from_recipe_tag_search_list = []
    recipes_from_recipe_ingredients_search_list = []

    for row in uva_dining_search_results:
        uva_dining_items.append(row)
    for row in recipe_search_results:
        recipe_items.append(row)

    #Getting all the info for recipes based on recipe tag search
    for r_id in recipe_tag_search_results:
        r_query = "SELECT * FROM recipes NATURAL JOIN recipe_instructions WHERE recipe_id = ?;"
        recipe_tag_results = database.execute_secure(True, r_query, r_id['recipe_id'])
        for i in recipe_tag_results:
            recipes_from_recipe_tag_search_list.append(i)
    #If the recipe_id does not exist in the search by recipe name and instruction, then add it to the overall recipe_items list of dictionaries
    for i in recipes_from_recipe_tag_search_list:
        key_check = "recipe_id"
        value_check = i["recipe_id"]
        value_exists = any(r[key_check] == value_check for r in recipe_items)
        if not value_exists:
            recipe_items.append(i)

    #Adding all the tags to the recipe items
    for recipe in recipe_items:
        recipe_tag_query = "SELECT tag FROM recipe_tags WHERE recipe_id = ?;"
        tags = database.execute_secure(True, recipe_tag_query, recipe["recipe_id"])
        recipe["tags"] = []
        for tag in tags:
            recipe["tags"].append(tag['tag'])


#Getting all the info for recipes based on recipe ingredients search
    for r_id in recipe_ingredients_search_results:
        r_query = "SELECT * FROM recipes NATURAL JOIN recipe_instructions WHERE recipe_id = ?;"
        recipe_ingredients_results = database.execute_secure(True, r_query, r_id['recipe_id'])
        for i in recipe_ingredients_results:
            recipes_from_recipe_ingredients_search_list.append(i)
    #If the recipe_id does not exist in the search by recipe name and instruction, then add it to the overall recipe_items list of dictionaries
    for i in recipes_from_recipe_ingredients_search_list:
        key_check = "recipe_id"
        value_check = i["recipe_id"]
        value_exists = any(r[key_check] == value_check for r in recipe_items)
        if not value_exists:
            recipe_items.append(i)

    #Adding all the ingredients to the recipe items
    for recipe in recipe_items:
        recipe_ingredients_query = "SELECT ingredient FROM recipe_ingredients2 WHERE recipe_id = ?;"
        ingredients = database.execute_secure(True, recipe_ingredients_query, recipe["recipe_id"])
        recipe["ingredients"] = []
        for ingredient in ingredients:
            recipe["ingredients"].append(ingredient['ingredient'])



    if len(username) > 0:
        # Find the meals that the user bookmarked
        bookmarked_meals = get_bookmarked_meals(database, username)

        # For each meal found, check if the user bookmarked it
        for menu_item in uva_dining_items:
            if menu_item["meal_id"] in bookmarked_meals:
                menu_item["is_bookmarked"] = True
            else:
                 menu_item["is_bookmarked"] = False
        #for recipe_item in recipe_items:
         #   if recipe_item["recipe_id"] in bookmarked_meals:
          #      recipe_item["is_bookmarked"] = True
           # else:
            #     recipe_item["is_bookmarked"] = False

    if len(username) > 0:
        bookmarked_recipes = get_bookmarked_recipes(database, username)

        for item in recipe_items:
            if item["recipe_id"] in bookmarked_recipes:
                item["is_bookmarked"] = True
            else:
                 item["is_bookmarked"] = False
                 
    database.close()

    context = {
        #"uva_dining_items" : uva_dining_search_results
        "uva_dining_items": uva_dining_items,
        "recipe_items": recipe_items,
    }
    return context

def search_results_view(request: HttpRequest) -> HttpRequest:
    keyword = request.GET.get('keyword', '')
    if request.COOKIES.get("user"):
        user = json.loads(request.COOKIES.get("user"))["username"]
        results = get_search_results(keyword, username=user)
    else:
        results = get_search_results(keyword)
    context = {'keyword' : keyword, **results}
    return render(request, 'hooeats_app/search-results.html', context)

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

def fetch_nutritional_data(request: HttpRequest, title: str, dining_hall: str, section: str) -> JsonResponse:
     query = "SELECT * FROM uva_descriptions WHERE title=? AND dining_hall=? AND section=?;"
     try:
          database = HooEatsDatabase(secure=True)
          nutritional_data = database.execute_secure(True, query, title, dining_hall, section)
          return JsonResponse(nutritional_data[0])
     except:
          error = {"result": "Database Error"}
          return JsonResponse(error)

def get_bookmarked_meals(database: HooEatsDatabase, username: str) -> List[Dict]:
     query = "SELECT meal_id FROM bookmark_meals WHERE username=?"
     meal_data =  database.execute_secure(True, query, username)
     meal_ids = []
     for meal in meal_data:
          meal_ids.append(meal["meal_id"])
     return meal_ids

def insert_bookmark(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    meal_id = data["meal_id"]
    username = json.loads(request.COOKIES.get("user"))["username"]
    query = "INSERT INTO bookmark_meals (username, meal_id) VALUES (?, ?);"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, query, username, meal_id)
        database.close()
        return JsonResponse({"result": "Insertion Successful"})
    except:
        return JsonResponse({"result": "Database Error"})

def remove_bookmark(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    meal_id = data["meal_id"]
    username = json.loads(request.COOKIES.get("user"))["username"] 
    query = "DELETE FROM bookmark_meals WHERE username=? AND meal_id=?;"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, query, username, meal_id)
        database.close()
        return JsonResponse({"result": "Deletion Successful"})
    except:
        return JsonResponse({"result": "Database Error"})
    
def get_bookmarked_recipes(database: HooEatsDatabase, username: str) -> List[Dict]:
    query = "SELECT recipe_id FROM bookmark_recipes WHERE username=?"
    recipe_data =  database.execute_secure(True, query, username)
    recipe_ids = []
    for recipe in recipe_data:
        recipe_ids.append(recipe["recipe_id"])
    return recipe_ids

def insert_bookmark_recipe(request: HttpRequest) -> JsonResponse:
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

def remove_bookmark_recipe(request: HttpRequest) -> JsonResponse:
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
    