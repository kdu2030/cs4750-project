import time
from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from database import HooEatsDatabase
from populator import insert_into_db

class CampusDishParser:

    def __init__(self, driver: WebDriver, dining_hall: str):
        self.driver = driver
        self.dining_hall = dining_hall
        if self.dining_hall == "Observatory Hill":
            self.url = "https://virginia.campusdish.com/LocationsAndMenus/ObservatoryHillDiningRoom"
        else:
            self.url = "https://virginia.campusdish.com/en/locationsandmenus/freshfoodcompany/"

    def open_change_modal(self):
        change_button = self.driver.find_element(
            By.CSS_SELECTOR, ".DateMealFilterButton")
        change_button.click()

    def close_change_modal(self):
        done_button = self.driver.find_element(By.CSS_SELECTOR, "button.Done")
        done_button.click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.HeaderItemNameLinkWeeklyMenu")))

    def change_to_weekly(self):
        weekly_option = self.driver.find_element(
            By.CSS_SELECTOR, "button.ButtonOutline")
        weekly_option.click()

    def open_meal_type_dropdown(self):
        meal_dropdown = self.driver.find_element(
            By.CSS_SELECTOR, "#modal-root > div > div > div > div > div.sc-gXmSlM.iTlHgL > div > div > div.sc-yeoIj.eGQvq > div > div")
        meal_dropdown.click()

    def get_meal_options(self) -> List[WebElement]:
        return self.driver.find_elements(By.CSS_SELECTOR, ".css-wuv0vk div")

    def get_meal_type_titles(self) -> List[str]:
        meal_type_options = self.get_meal_options()
        meal_types = []
        for meal_type_option in meal_type_options:
            meal_types.append(meal_type_option.get_attribute("innerText"))
        return meal_types

    def get_num_days(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".flOORh"))

    def show_all(self):
        see_all_buttons = self.driver.find_elements(
            By.CSS_SELECTOR, "button[title=\"See More\"]")
        for button in see_all_buttons:
            self.driver.execute_script("arguments[0].click()", button)

    def get_meal_buttons(self, day_of_week: int) -> Dict[str, WebElement]:
        section_elements = self.driver.find_elements(
            By.CSS_SELECTOR, f".flOORh:nth-child({day_of_week}) .StationHeaderTitle")
        sections = []
        for section in section_elements:
            sections.append(section.get_attribute("innerText"))
        meal_buttons = {}
        for i, section in enumerate(sections):
            meal_buttons[section] = self.driver.find_elements(
                By.CSS_SELECTOR, f".flOORh:nth-child({day_of_week}) .jCLkpp:nth-child({i+2}) .HeaderItemNameLinkWeeklyMenu")
        return meal_buttons


    def get_num(self, nutritional_value: str) -> float:
        space_index = nutritional_value.find(" ")
        if space_index == -1 or not nutritional_value[:space_index].isdigit():
            return 0.0
        return float(space_index)

    
    def get_meal(self, day_of_week: int, section: str, meal_type: str, meal_button: WebElement):
        meal = {}

        day_of_week_header = self.driver.find_element(
            By.CSS_SELECTOR, f".flOORh:nth-child({day_of_week}) h2")
        meal["day_of_week"] = day_of_week_header.get_attribute(
            "innerText")

        meal_button.click()
        # Need to wait for meal data to load
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.ModalProductDescriptionContent")))

        meal["title"] = meal_button.accessible_name

        description = self.driver.find_element(
            By.CSS_SELECTOR, "div.ModalProductDescriptionContent")
        meal["description"] = description.get_attribute("innerText")

        meal["type"] = meal_type

        meal["section"] = section

        serving_size_element = self.driver.find_element(
            By.CSS_SELECTOR, "div.ModalProductServingSize")
        # Get rid of "Serving Size " in the text
        meal["serving_size"] = serving_size_element.get_attribute("innerText")[
            13:]

        calories_span = self.driver.find_element(
            By.CSS_SELECTOR, "li.Calories > span")
        meal["calories"] = float(calories_span.get_attribute("innerText"))

        calories_from_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Calories.From.Fat > span")
        calories_from_fat_text = calories_from_fat_span.get_attribute(
            "innerText")
        if calories_from_fat_text.isdigit():
            meal["calories_from_fat"] = float(calories_from_fat_text)
        else:
            meal["calories_from_fat"] = 0.0

        total_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Total.Fat > span")
        meal["total_fat"] = self.get_num(total_fat_span.get_attribute("innerText"))

        saturated_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Saturated.Fat span.SpanNutrition")
        meal["saturated_fat"] = self.get_num(saturated_fat_span.get_attribute(
            "innerText"))

        trans_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Trans.Fat span.SpanNutrition")
        meal["saturated_fat"] = self.get_num(saturated_fat_span.get_attribute(
            "innerText"))

        cholesterol_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Cholesterol span")
        meal["cholesterol"] = self.get_num(cholesterol_span.get_attribute("innerText"))

        sodium_span = self.driver.find_element(By.CSS_SELECTOR, ".Sodium span")
        meal["sodium"] = self.get_num(sodium_span.get_attribute("innerText"))

        total_carbs_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Total.Carbohydrates span")
        meal["total_carbohydrates"] = self.get_num(total_carbs_span.get_attribute(
            "innerText"))

        dietary_fiber_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Dietary.Fiber span")
        meal["dietary_fiber"] = self.get_num(dietary_fiber_span.get_attribute(
            "innerText"))

        sugar_span = self.driver.find_element(By.CSS_SELECTOR, ".Sugars span")
        meal["sugar"] = self.get_num(sugar_span.get_attribute("innerText"))

        protein_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Protein > span")
        meal["protein"] = self.get_num(protein_span.get_attribute("innerText"))

        close_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[aria-label=\"Close\"]")
        close_button.click()

        return meal

    def add_cookies(self):
        date = datetime.now()
        # Get rid of mailing list promotion
        self.driver.add_cookie(
            {"name": "IsShownMailSubscriptionWidget", "value": ""})
        # Get rid of asking for cookies
        self.driver.add_cookie({"name": "OptanonConsent", "value": ""})
        self.driver.add_cookie(
            {"name": "OptanonAlertBoxClosed", "value": date.strftime("%Y-%m-%dT%H:%M:%S")})
        self.driver.refresh()

    def get_all_meals(self, meal_type: str) -> List[Dict]:

        self.show_all()

        meals = []
        num_days = self.get_num_days()

        for i in range(1, num_days+1):
            meal_buttons = self.get_meal_buttons(i)

            for section_title in meal_buttons.keys():
                section_meal_buttons = meal_buttons[section_title]
                for button in section_meal_buttons:
                    try:
                        meal = self.get_meal(
                            i, section_title, meal_type, button)
                        meals.append(meal)
                    except:
                        continue
        
        insert_into_db(meals, self.dining_hall)
        return meals

    def change_meal(self, meal_title: str):
        self.open_change_modal()
        self.change_to_weekly()
        self.open_meal_type_dropdown()
        meal_options = self.get_meal_options()
        for meal_option in meal_options:
            if meal_option.get_attribute("innerText") == meal_title:
                meal_option.click()
                break
        self.close_change_modal()

    def parse_menu(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.add_cookies()
        self.open_change_modal()
        self.change_to_weekly()

        # List of Meal Option Buttons in change dropdown
        self.open_meal_type_dropdown()
        meal_types = self.get_meal_type_titles()
        self.get_meal_options()[0].click()
        self.close_change_modal()

        all_meals = []

        for i, meal_type in enumerate(meal_types):
            if i != 0:
                self.driver.refresh()
                self.change_meal(meal_type)
            # Actual meal type
            choosen_meal_type = self.driver.find_element(
                By.CSS_SELECTOR, ".ChoosenMeal").get_attribute("innerText")
            all_meals.append(self.get_all_meals(choosen_meal_type))

        return all_meals

    def get_week_dates(self) -> Dict[str, str]:
        today = datetime.now()
        start_of_week = today - timedelta(days=((today.weekday())))
        date_strs = {}
        days_of_week = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            date_strs[days_of_week[i]] = date.strftime("%Y-%m-%d")
        return date_strs

    def esc_apostrophes(self, meal: Dict[str, str]):
        for key in meal.keys():
            if type(meal[key]) == str and meal[key].find("'") != -1:
                meal[key] = meal[key].replace("'", "''");
        return meal



def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_driver = Service("../chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_driver, options=chrome_options)
    parser = CampusDishParser(driver, "Fresh Food Company")
    print(parser.parse_menu())


if __name__ == "__main__":
    main()
