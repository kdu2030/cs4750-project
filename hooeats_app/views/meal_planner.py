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

        # Necessary because can't convert datetime objects to JSON
        context["selected_meal_plan_data"] = copy.deepcopy(
            context["selected_meal_plan"])
        context["selected_meal_plan_data"]["week_start"] = context["selected_meal_plan_data"]["week_start"].strftime(
            "%m/%d/%Y")

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


def insert_uva_meal(request: HttpRequest) -> HttpResponse:
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
        return JsonResponse({"result": "Insertion successful"})
    except:
        print_exc()
        return JsonResponse({"result": "Database error"})
     
    
