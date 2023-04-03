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
    database = HooEatsDatabase()
    for meal in meal_data:
        meal = esc_apostrophes(meal)

        meal_date = date_strs[meal["day_of_week"]]

        uva_description_select = "SELECT * FROM uva_descriptions WHERE title='{title}' AND section='{section}' AND dining_hall='{dining_hall}';".format(title=meal["title"], section=meal["section"], dining_hall=dining_hall);
        select_results = database.execute(uva_description_select, expect_results=True)
        if len(select_results) == 0:
            uva_description_insert = "INSERT INTO uva_descriptions (title, dining_hall, section, description, serving_size, calories, calories_from_fat, total_fat, saturated_fat, sugar, protein, dietary_fiber, total_carbohydrates, sodium, cholestorol) VALUES ('{title}', '{description}', '{dining_hall}', '{section}', '{serving_size}', {calories:.2f}, {calories_from_fat:.2f}, {total_fat:.2f}, {saturated_fat:.2f}, {sugar:.2f}, {protein:.2f}, {dietary_fiber:.2f}, {total_carbohydrates:.2f}, {sodium:.2f}, {cholesterol:.2f})".format(title=meal["title"], dining_hall=dining_hall, section=meal["section"], description=meal["description"], serving_size=meal["serving_size"], calories=meal["calories"], calories_from_fat=meal["calories_from_fat"], total_fat=meal["total_fat"], saturated_fat=meal["saturated_fat"], sugar=meal["sugar"], protein=meal["protein"], dietary_fiber=meal["dietary_fiber"], total_carbohydrates=meal["total_carbohydrates"], sodium=meal["sodium"], cholesterol=meal["cholesterol"])
            database.execute(uva_description_insert, expect_results=False)


        uva_meals_query = "INSERT INTO uva_meals (title, dining_hall, section, meal_type, meal_date) VALUES ('{title}', '{dining_hall}', '{section}', '{meal_type}', '{meal_date}')".format(title=meal["title"], dining_hall=dining_hall, section=meal["section"], meal_type=meal["type"], meal_date=meal_date)
        database.execute(uva_meals_query, expect_results=False)
    
    database.close()
    