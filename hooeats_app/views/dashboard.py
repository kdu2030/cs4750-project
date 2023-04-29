
import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from hooeats_app.db_utils.database import HooEatsDatabase
from traceback import print_exc

def dashboard(request: HttpRequest) -> HttpResponse:
    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    user = json.loads(request.COOKIES.get("user"))["username"]
    context = {}
    meal_plans_query = "SELECT plan_name, plan_id, week_start FROM meal_plan WHERE username = ? ORDER BY week_start DESC;"
    bookmark_meals_query = "SELECT meal_id, title, dining_hall, section FROM bookmark_meals NATURAL JOIN uva_meals WHERE username= ?;"
    bookmark_recipes_query = "SELECT recipe_id, recipe_name FROM bookmark_recipes NATURAL JOIN recipes WHERE username = ?;"
    
    try:
        database = HooEatsDatabase(secure=True)
        context["meal_plans"] = database.execute_secure(True, meal_plans_query, user)
        context["bookmark_meals"] = database.execute_secure(True, bookmark_meals_query, user)
        context["bookmark_recipes"] = database.execute_secure(True, bookmark_recipes_query, user)
        database.close()
    except:
        print_exc()
        context["error"] = "Failed to Fetch Data"
        
    return render(request, "hooeats_app/dashboard.html", context=context)