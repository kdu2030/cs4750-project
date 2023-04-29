from database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta

def get_week_dates() -> Dict[str, str]:
    today = datetime.now()
    start_of_week = today - timedelta(days=((today.weekday())))
    date_strs = {}
    days_of_week = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        date_strs[days_of_week[i]] = date.strftime("%Y-%m-%d")
    return date_strs

def esc_apostrophes(meal: Dict[str, str]):
    for key in meal.keys():
        if type(meal[key]) == str and meal[key].find("'") != -1:
            meal[key] = meal[key].replace("'", "''");
    return meal
    
def insert_into_db(meal_data: List[Dict[str, Dict]], dining_hall: str):
    date_strs = get_week_dates()
    database = HooEatsDatabase(secure=True)
    for meal in meal_data:
        meal = esc_apostrophes(meal)

        meal_date = date_strs[meal["day_of_week"]]

        uva_description_select = "SELECT * FROM uva_descriptions WHERE title=? AND section=? AND dining_hall=?;"
        select_results = database.execute_secure(True, uva_description_select, meal["title"], meal["section"], dining_hall)
        if len(select_results) == 0:
            uva_description_insert = "INSERT INTO uva_descriptions (title, dining_hall, section, description, serving_size, calories, calories_from_fat, total_fat, saturated_fat, sugar, protein, dietary_fiber, total_carbohydrates, sodium, cholesterol) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
            database.execute_secure(False, uva_description_insert, meal["title"], dining_hall, meal["section"], meal["description"], meal["serving_size"], meal["calories"], meal["calories_from_fat"], meal["total_fat"], meal["saturated_fat"], meal["sugar"], meal["protein"], meal["dietary_fiber"], meal["total_carbohydrates"], meal["sodium"], meal["cholesterol"])


        uva_meals_query = "INSERT INTO uva_meals (title, dining_hall, section, meal_type, meal_date) VALUES (?, ?, ?, ?, ?)"
        database.execute_secure(False, uva_meals_query, meal["title"], dining_hall, meal["section"], meal["type"], meal_date)
    
    database.close()
    