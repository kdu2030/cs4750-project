from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json
from hooeats_app.date_utils.week_dates import get_week_dates

def get_bookmarked_meals(database: HooEatsDatabase, username: str) -> List[Dict]:
     query = "SELECT meal_id FROM bookmark_meals WHERE username=?"
     meal_data =  database.execute_secure(True, query, username)
     meal_ids = []
     for meal in meal_data:
          meal_ids.append(meal["meal_id"])
     return meal_ids

def get_dining_hall_data(dining_hall: str, selected_date:str = "", selected_meal: str="", username: str = ""):
    if selected_date == "":
        selected_date = datetime.now().strftime("%m/%d/%Y")
    
    # Create the data for the date selector dropdown
    week_dates = get_week_dates(selected_date)
    date_links = []
    for week_date in week_dates:
        link = week_date.replace("/", "-")
        date_dict = {
             "date_text": week_date,
             "date_link": link,
        }
        date_links.append(date_dict)
    
    section_query = "SELECT DISTINCT section FROM uva_meals WHERE dining_hall=?;"
    meal_type_query = "SELECT DISTINCT meal_type FROM uva_meals WHERE dining_hall=? AND meal_date=? "

    database = HooEatsDatabase(secure=True)
    sections = database.execute_secure(True, section_query, dining_hall)
    meal_types = database.execute_secure(True, meal_type_query, dining_hall, datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d"))

    if selected_meal == "" and len(meal_types) > 0:
        selected_meal = meal_types[0]["meal_type"]

    all_menu_items = []

    # For each section, get the meals belonging to the section
    for section_row in sections:
         date = datetime.strptime(selected_date, "%m/%d/%Y")
         date_str = datetime.strftime(date, "%Y-%m-%d")
         item_query = "SELECT uva_meals.meal_id, uva_meals.title, uva_meals.section, uva_descriptions.description FROM uva_meals NATURAL JOIN uva_descriptions WHERE meal_date=? AND dining_hall=? AND section=?"
         items = database.execute_secure(True, item_query, date_str, dining_hall.title(), section_row["section"])
         all_menu_items.extend(items)
    

    if len(username) > 0:
        # Find the meals that the user bookmarked
        bookmarked_meals = get_bookmarked_meals(database, username)

        # For each meal found, check if the user bookmarked it
        for menu_item in all_menu_items:
            if menu_item["meal_id"] in bookmarked_meals:
                menu_item["is_bookmarked"] = True
            else:
                 menu_item["is_bookmarked"] = False

    all_sections = []
    for section in sections:
         all_sections.append(section["section"])
    

    database.close()

    context = {
        "dining_hall_title": dining_hall.title(),
        "selected_date": selected_date,
        "selected_date_link": selected_date.replace("/", "-"),
        "date_links": date_links,
        "sections": all_sections,
        "menu_items": all_menu_items,
        "selected_meal": selected_meal.title(),
        "meal_types": meal_types
    }
    return context


def dining_hall(request: HttpRequest, dining_hall: str) -> HttpResponse:
    if request.COOKIES.get("user"):
         user = json.loads(request.COOKIES.get("user"))["username"]
         context = get_dining_hall_data(dining_hall, username=user)
    else:
        context = get_dining_hall_data(dining_hall)
    return render(request, "hooeats_app/dining-hall.html", context=context)

def dining_hall_date(request: HttpRequest, dining_hall: str, date_str: str) -> HttpResponse:
    date_no_slashes = date_str.replace("-", "/")
    if request.COOKIES.get("user"):
         user = json.loads(request.COOKIES.get("user"))["username"]
         context = get_dining_hall_data(dining_hall, date_no_slashes, username=user)
    else:
        context = context = get_dining_hall_data(dining_hall, date_no_slashes)
    return render(request, "hooeats_app/dining-hall.html", context=context)

def dining_hall_meal(request: HttpRequest, dining_hall: str, date_str: str, meal_type: str) -> HttpResponse:
    date_no_slashes = date_str.replace("-", "/")
    if request.COOKIES.get("user"):
         user = json.loads(request.COOKIES.get("user"))["username"]
         context = get_dining_hall_data(dining_hall, date_no_slashes, meal_type, username=user)
    else:
        context = context = get_dining_hall_data(dining_hall, date_no_slashes, meal_type)
    return render(request, "hooeats_app/dining-hall.html", context=context)

def fetch_nutritional_data(request: HttpRequest, title: str, dining_hall: str, section: str) -> JsonResponse:
     query = "SELECT * FROM uva_descriptions WHERE title=? AND dining_hall=? AND section=?;"
     try:
          database = HooEatsDatabase(secure=True)
          nutritional_data = database.execute_secure(True, query, title, dining_hall, section)
          return JsonResponse(nutritional_data[0])
     except:
          error = {"result": "Database Error"}
          return JsonResponse(error)

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
        

