import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from typing import Dict

from django.urls import reverse
from hooeats_app.db_utils.database import HooEatsDatabase
from datetime import datetime, timedelta
from hooeats_app.date_utils.week_dates import get_week_start
from traceback import print_exc
import copy


def get_meal_plan(username: str) -> Dict:
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

        context["selected_meal_plan"] = meal_plans[0]

        # Get the meal plan items
        uva_meals_in_plan_query = "SELECT * FROM meal_item NATURAL JOIN uva_meals NATURAL JOIN uva_descriptions WHERE plan_id = ?"
        uva_meals_in_plan = database.execute_secure(True, uva_meals_in_plan_query, context["selected_meal_plan"]["plan_id"])
        for uva_meal in uva_meals_in_plan:
            uva_meal["week_offset"] = (uva_meal["date"] - context["selected_meal_plan"]["week_start"]).days
            uva_meal["meal_date"] = uva_meal["meal_date"].strftime("%m/%d/%Y")

        # Get data for meal plan items
        uva_meals_data = copy.deepcopy(uva_meals_in_plan)
        columns = {"plan_id", "item_id", "date", "plan_meal_type", "week_offset"}
        for meal_data in uva_meals_data:
            keys = list(meal_data.keys())
            for column in keys:
                if column in columns:
                    del meal_data[column]
                

        
        context["uva_meals_in_plan"] = uva_meals_in_plan

        # Get the UVA meals for only the week that the meal plan is for
        bookmarked_meals_query = "SELECT * FROM bookmark_meals NATURAL JOIN uva_meals NATURAL JOIN uva_descriptions WHERE username=? AND meal_date BETWEEN ? AND ?;"
        bookmarked_meals = database.execute_secure(True, bookmarked_meals_query, username, context["selected_meal_plan"]["week_start"].strftime(
            "%Y-%m-%d"), (context["selected_meal_plan"]["week_start"] + timedelta(days=6)).strftime("%Y-%m-%d"))
        for bookmarked_meal in bookmarked_meals:
            bookmarked_meal["meal_date"] = bookmarked_meal["meal_date"].strftime(
                "%m/%d/%Y")
        context["bookmarked_meals"] = bookmarked_meals
        
        database.close()

        # Union together bookmarked_meals and uva_meals_data
        all_uva_meals = set()
        bookmarked_meals_set = set()
        for uva_meal in uva_meals_data:
            all_uva_meals.add(json.dumps(uva_meal))

        for bookmarked_meal in bookmarked_meals:
            bookmarked_meals_set.add(json.dumps(bookmarked_meal))
        
        all_uva_meals = all_uva_meals.union(bookmarked_meals_set)
        
        all_uva_meals = list(all_uva_meals)
        for i, meal_str in enumerate(all_uva_meals):
            all_uva_meals[i] = json.loads(meal_str)
            
        context["all_uva_meals_data"] = all_uva_meals

        # Necessary because can't convert datetime objects to JSON
        context["selected_meal_plan_data"] = copy.deepcopy(
            context["selected_meal_plan"])
        context["selected_meal_plan_data"]["week_start"] = context["selected_meal_plan_data"]["week_start"].strftime(
            "%m/%d/%Y")

        #TODO: Union together bookmarked_meals and uva_meals - This may require a new query
        return context
    except:
        print_exc()


def meal_planner(request: HttpRequest) -> HttpResponse:
    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    user = json.loads(request.COOKIES.get("user"))["username"]
    context = get_meal_plan(user)
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
    # TODO: Should redirect based on plan_id
    return redirect(reverse("meal_planner"))

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
        return JsonResponse({"result": "Database error"})
     
    
