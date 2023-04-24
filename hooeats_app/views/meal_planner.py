import json
from django.http import HttpRequest, HttpResponse
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
        meal_plans_query = "SELECT * from meal_plan WHERE username = ? ORDER BY week_start DESC"
        meal_plans = database.execute_secure(True, meal_plans_query, username)
        context["meal_plans"] = meal_plans

        if len(meal_plans) == 0:
             context["selected_meal_plan"] = {}
             database.close()
             return context
        
        context["selected_meal_plan"] = meal_plans[0]
        
        bookmarked_meals_query = "SELECT * FROM bookmark_meals NATURAL JOIN uva_meals NATURAL JOIN uva_descriptions WHERE username=? AND meal_date BETWEEN ? AND ?;"
        bookmarked_meals = database.execute_secure(True, bookmarked_meals_query, username, context["selected_meal_plan"]["week_start"].strftime("%Y-%m-%d"), (context["selected_meal_plan"]["week_start"] + timedelta(days=6)).strftime("%Y-%m-%d"))
        for bookmarked_meal in bookmarked_meals:
            bookmarked_meal["meal_date"] = bookmarked_meal["meal_date"].strftime("%m/%d/%Y")
        context["bookmarked_meals"] = bookmarked_meals
        database.close()

        context["selected_meal_plan_data"] = copy.deepcopy(context["selected_meal_plan"])
        context["selected_meal_plan_data"]["week_start"] = context["selected_meal_plan_data"]["week_start"].strftime("%m/%d/%Y")

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
    database.execute_secure(True, create_plan_query, username, plan_name, week_start)
    database.close()
    return redirect(reverse("meal_planner"))
    
