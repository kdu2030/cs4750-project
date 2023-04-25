from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json

def get_search_results(request: HttpRequest, keyword: str) -> JsonResponse:
    recipe_query = "SELECT * FROM recipe JOIN recipe_tags JOIN recipe_ingredients '\
    WHERE recipe_name LIKE ? OR steps LIKE ? OR ingredient LIKE ? OR tag LIKE ? '\
    UNION  '\
    SELECT * FROM uva_meals JOIN uva_descriptions '\
    WHERE title LIKE ? OR station LIKE ? OR description LIKE ? OR dining_hall LIKE ?"
    try:
        database = HooEatsDatabase(secure=True)
        recipe_search_result_data = database.execute_secure(True, recipe_query, keyword, keyword, keyword, keyword)
        dining_hall_search_result_data = database.execute_secure(True, recipe_query, keyword, keyword, keyword, keyword)
        return JsonResponse([recipe_search_result_data, dining_hall_search_result_data])
    except:
        error = {"result": "Database Error"}
        return JsonResponse(error)

def get_search_results(keyword: str, username: str = ""):
    #recipe_search_query = "SELECT * FROM recipe JOIN recipe_tags JOIN recipe_ingredients '\
    #WHERE recipe_name LIKE ? OR steps LIKE ? OR ingredient LIKE ? OR tag LIKE ? '\
    
    uva_dining_search_query = "SELECT * FROM uva_meals JOIN uva_descriptions WHERE uva_meals.title LIKE ? OR uva_meals.section LIKE ? OR uva_descriptions.description LIKE ? OR uva_meals.dining_hall LIKE ?"

    database = HooEatsDatabase(secure=True)
    uva_dining_search_results = database.execute_secure(True, uva_dining_search_query, keyword, keyword, keyword, keyword)
    #recipe_search_results = database.execute_secure(True, recipe_search_query, keyword)

    uva_dining_items = []

#i need uva_descriptions.description, uva_descriptions.calories, uva_meals.title, uva_meals.meal_id
    for row in uva_dining_search_results:
         #fix query
         #? may not be working properly??
         uva_dining_item_query = "SELECT uva_meals.meal_id, uva_meals.title, uva_descriptions.description, uva_descriptions.calories FROM uva_meals NATURAL JOIN uva_descriptions WHERE uva_meals.title = ? OR uva_descriptions.title = ?"
         items = database.execute_secure(True, uva_dining_item_query, row["title"], row["title"])
         uva_dining_items.extend(items)
    

    if len(username) > 0:
        # Find the meals that the user bookmarked
        bookmarked_meals = get_bookmarked_meals(database, username)

        # For each meal found, check if the user bookmarked it
        for menu_item in uva_dining_items:
            if menu_item["meal_id"] in bookmarked_meals:
                menu_item["is_bookmarked"] = True
            else:
                 menu_item["is_bookmarked"] = False

    database.close()

    context = {
        "uva_dining_items": uva_dining_items,
    }
    return context

def search_results_view(request: HttpRequest) -> HttpRequest:
    keyword = request.GET.get('keyword', '')
    if request.COOKIES.get("user"):
        user = json.loads(request.COOKIES.get("user"))["username"]
        results = get_search_results(keyword, username=user)
    else:
        results = get_search_results(keyword)
    context = {'results': results, 'keyword' : keyword}
    return render(request, 'hooeats_app/search-results.html', context)

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