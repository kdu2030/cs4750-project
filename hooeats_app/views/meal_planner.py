import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from typing import Dict, List

from django.urls import reverse
from hooeats_app.db_utils.database import HooEatsDatabase
from datetime import datetime, timedelta
from hooeats_app.date_utils.week_dates import get_week_start, get_week_dates
from traceback import print_exc
import copy

def union_dict_lists(dicts1: List[Dict], dicts2: List[Dict]) -> List[Dict]:
    combined_dicts = set()
    dict2_strs = set()
    for dict1_dict in dicts1:
        combined_dicts.add(json.dumps(dict1_dict))

    for dict2_dict in dicts2:
        dict2_strs.add(json.dumps(dict2_dict))
    
    combined_dicts = combined_dicts.union(dict2_strs)
    
    combined_dicts = list(combined_dicts)
    for i, meal_str in enumerate(combined_dicts):
        combined_dicts[i] = json.loads(meal_str)
        
    return combined_dicts

def delete_keys(dict_list: List[Dict], *keys_to_delete: List[str]):
    small_dict_list = copy.deepcopy(dict_list)
    columns = set(keys_to_delete)
    for large_dict in small_dict_list:
        keys = list(large_dict.keys())
        for column in keys:
            if column in columns:
                del large_dict[column]
    return small_dict_list


def get_meal_plan(username: str, plan_id:int = -1) -> Dict:
    context = {}
    try:
        database = HooEatsDatabase(secure=True)

        # Get the meal plans that a user has
        meal_plans_query = "SELECT * from meal_plan WHERE username = ? ORDER BY week_start DESC"
        meal_plans = database.execute_secure(True, meal_plans_query, username)
        context["meal_plans"] = meal_plans

        # Check if the user doesn't have any meal plans
        if len(meal_plans) == 0:
             context["selected_meal_plan"] = {}
             database.close()
             return context
            
        # The user is not viewing a specific meal plan
        if plan_id == -1:
            context["selected_meal_plan"] = meal_plans[0]
        else:
            for i, meal_plan in enumerate(meal_plans):
                if meal_plan["plan_id"] == plan_id:
                    context["selected_meal_plan"] = meal_plans[i]

        # Get the meal plan items
        uva_meals_in_plan_query = "SELECT * FROM meal_item NATURAL JOIN uva_meals NATURAL JOIN uva_descriptions WHERE plan_id = ?"
        uva_meals_in_plan = database.execute_secure(True, uva_meals_in_plan_query, context["selected_meal_plan"]["plan_id"])
        for uva_meal in uva_meals_in_plan:
            uva_meal["week_offset"] = (uva_meal["date"] - context["selected_meal_plan"]["week_start"]).days
            uva_meal["meal_date"] = uva_meal["meal_date"].strftime("%m/%d/%Y")

        # Get recipes that are in the selected meal plan
        recipes_in_plan_query = "SELECT * FROM recipe_item NATURAL JOIN recipes NATURAL JOIN recipe_images WHERE plan_id = ?;"
        recipes_in_plan = database.execute_secure(True, recipes_in_plan_query, context["selected_meal_plan"]["plan_id"])
        for recipe in recipes_in_plan:
            recipe["week_offset"] = (recipe["date"] - context["selected_meal_plan"]["week_start"]).days
    

        uva_meals_data = delete_keys(uva_meals_in_plan, "plan_id", "item_id", "date", "plan_meal_type", "week_offset")
        recipes_in_plan_data = delete_keys(recipes_in_plan, "plan_id", "item_id", "date", "plan_meal_type", "week_offset")

        
        context["uva_meals_in_plan"] = uva_meals_in_plan
        context["recipes_in_plan"] = recipes_in_plan

        # Get the UVA meals for only the week that the meal plan is for
        bookmarked_meals_query = "SELECT * FROM bookmark_meals NATURAL JOIN uva_meals NATURAL JOIN uva_descriptions WHERE username=? AND meal_date BETWEEN ? AND ?;"
        bookmarked_meals = database.execute_secure(True, bookmarked_meals_query, username, context["selected_meal_plan"]["week_start"].strftime(
            "%Y-%m-%d"), (context["selected_meal_plan"]["week_start"] + timedelta(days=6)).strftime("%Y-%m-%d"))
        for bookmarked_meal in bookmarked_meals:
            bookmarked_meal["meal_date"] = bookmarked_meal["meal_date"].strftime(
                "%m/%d/%Y")
        context["bookmarked_meals"] = bookmarked_meals

        # Get bookmarked recipes
        bookmarked_recipes_query = "SELECT * FROM bookmark_recipes NATURAL JOIN recipes NATURAL JOIN recipe_images WHERE username=?;"
        bookmarked_recipes = database.execute_secure(True, bookmarked_recipes_query, username)
        context["bookmarked_recipes"] = bookmarked_recipes



        database.close()

        

        # Union together bookmarked_meals and uva_meals_data
        context["all_uva_meals_data"] = union_dict_lists(uva_meals_data, bookmarked_meals)
        context["all_recipes_data"] = union_dict_lists(recipes_in_plan_data, bookmarked_recipes)

        # Necessary because can't convert datetime objects to JSON
        context["selected_meal_plan_data"] = copy.deepcopy(
            context["selected_meal_plan"])
        context["selected_meal_plan_data"]["week_start"] = context["selected_meal_plan_data"]["week_start"].strftime(
            "%m/%d/%Y")
        
        context["range"] = list(range(0, 7))

        # Get Dates For Headers
        week_dates = get_week_dates(context["selected_meal_plan_data"]["week_start"],"%m/%d/%Y")
        context["week_dates"] = []
        for week_date in week_dates:
            context["week_dates"].append(week_date)

        return context
    except:
        print_exc()
        context["error"] = "Unable to fetch meal plans"
        return context


def meal_planner(request: HttpRequest) -> HttpResponse:
    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    user = json.loads(request.COOKIES.get("user"))["username"]
    context = get_meal_plan(user)
    return render(request, "hooeats_app/meal-planner.html", context=context)

def meal_plan_specific(request: HttpRequest, plan_id: int) -> HttpResponse:
    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    user = json.loads(request.COOKIES.get("user"))["username"]
    context = get_meal_plan(user, plan_id)
    return render(request, "hooeats_app/meal-planner.html", context=context)


def create_meal_plan(request: HttpRequest) -> HttpResponse:
    if request.COOKIES.get("user") is None:
        return redirect(reverse("signin"))
    username = json.loads(request.COOKIES.get("user"))["username"]
    week_date = request.POST.get("week-start")
    plan_name = request.POST.get("plan-name")
    week_start = get_week_start(week_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    create_plan_query = "INSERT INTO meal_plan (username, plan_name, week_start) VALUES (?, ?, ?);"
    database = HooEatsDatabase(secure=True)
    database.execute_secure(True, create_plan_query,
                            username, plan_name, week_start)
    database.close()
    return redirect(reverse("meal_planner"))

def update_meal_plan(request: HttpRequest) -> HttpResponse:
    plan_name = request.POST.get("plan_name")
    plan_id = request.POST.get("plan_id")
    update_meal_plan_query = "UPDATE meal_plan SET plan_name=? WHERE plan_id=?;"
    database = HooEatsDatabase(secure=True)
    database.execute_secure(True, update_meal_plan_query, plan_name, plan_id)
    database.close()
    return redirect(reverse("specific_meal_plan", kwargs={"plan_id", plan_id}))

def delete_meal_plan(request: HttpRequest) -> HttpResponse:
    plan_id = request.POST.get("plan_id")
    delete_meal_plan_query = "DELETE FROM meal_plan WHERE plan_id=?;"
    database = HooEatsDatabase(secure=True)
    database.execute_secure(True, delete_meal_plan_query, plan_id)
    database.close()
    return redirect(reverse("meal_planner"))

def insert_uva_meal(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    max_id_query = "SELECT MAX(item_id) FROM meal_item;"
    create_meal_item_query = "INSERT INTO meal_item (plan_id, item_id, meal_id, date, plan_meal_type) VALUES (?, ?, ?, ?, ?)"
    try:
        database = HooEatsDatabase(secure=True)
        max_id = database.execute(max_id_query, expect_results=True)
        if max_id[0]["MAX(item_id)"] is None:
            new_id = 1
        else:
            new_id = max_id[0]["MAX(item_id)"] + 1
        database.execute_secure(False, create_meal_item_query, data["plan_id"], new_id, data["meal_id"], data["date"], data["meal_type"])
        database.close()
        return JsonResponse({"result": new_id})
    except:
        print_exc()
        return JsonResponse({"result": "Database error"})
    
def update_uva_meal(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    update_query = "UPDATE meal_item SET date=?, plan_meal_type=? WHERE item_id=?"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, update_query, data["date"], data["plan_meal_type"], data["item_id"])
        database.close()
        return JsonResponse({"result": "Update successful"})
    except:
        return JsonResponse({"result": "Database error"})

def delete_uva_meal(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    delete_query = "DELETE FROM meal_item WHERE item_id=?"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, delete_query, data["item_id"])
        database.close()
        return JsonResponse({"result": "Delete successful"})
    except:
        print_exc()
        return JsonResponse({"result": "Database error"})
    

def insert_recipe(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    max_id_query = "SELECT MAX(item_id) FROM recipe_item;"
    create_meal_item_query = "INSERT INTO recipe_item (plan_id, item_id, recipe_id, date, plan_meal_type) VALUES (?, ?, ?, ?, ?)"
    try:
        database = HooEatsDatabase(secure=True)
        max_id = database.execute(max_id_query, expect_results=True)
        if max_id[0]["MAX(item_id)"] is None:
            new_id = 1
        else:
            new_id = max_id[0]["MAX(item_id)"] + 1
        database.execute_secure(False, create_meal_item_query, data["plan_id"], new_id, data["recipe_id"], data["date"], data["meal_type"])
        database.close()
        return JsonResponse({"result": new_id})
    except:
        print_exc()
        return JsonResponse({"result": "Database error"})
    
def update_recipe(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    update_query = "UPDATE recipe_item SET date=?, plan_meal_type=? WHERE item_id=?"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, update_query, data["date"], data["plan_meal_type"], data["item_id"])
        database.close()
        return JsonResponse({"result": "Update successful"})
    except:
        print_exc()
        return JsonResponse({"result": "Database error"})
    
def delete_recipe(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    delete_query = "DELETE FROM recipe_item WHERE item_id=?"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, delete_query, data["item_id"])
        database.close()
        return JsonResponse({"result": "Delete successful"})
    except:
        return JsonResponse({"result": "Database error"})
     
    
