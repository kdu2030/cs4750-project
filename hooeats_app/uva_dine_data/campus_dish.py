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

    # def change_meals(self, index: int = 0):
    #     meal_dropdown = self.driver.find_element(By.CSS_SELECTOR, ".sc-hAsxaJ .css-1t70p0u-control")
    #     meal_dropdown.click()
    #     meal_option = self.driver.find_element(By.CSS_SELECTOR, f".css-wuv0vk > #react-select-2-option-{index}")
    #     meal_option.click()
    def open_meal_type_dropdown(self):
        meal_dropdown = self.driver.find_element(
            By.CSS_SELECTOR, "#modal-root > div > div > div > div > div.sc-gXmSlM.iTlHgL > div > div > div.sc-yeoIj.eGQvq > div > div")
        meal_dropdown.click()
        # options = self.get_meal_type_titles(self.driver.find_elements(By.CSS_SELECTOR, ".css-wuv0vk div"))
        # self.get_meal_options()[0].click()
        # return options

    def get_meal_options(self) -> List[WebElement]:
        return self.driver.find_elements(By.CSS_SELECTOR, ".css-wuv0vk div")
        # return self.driver.find_elements(By.CSS_SELECTOR, ".css-26l3qy-menu")

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
        # num_sections = len(self.driver.find_elements(By.CSS_SELECTOR, f".sc-ktCSKO > .nmzKf:nth-child(day_of_week) > .eZlfSI"))
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

        # return self.driver.find_elements(By.CSS_SELECTOR, f".sc-ktCSKO > .nmzKf:nth-child({day_of_week}) button.HeaderItemNameLinkWeeklyMenu")

    def get_meal_data(self, day_of_week: int, section: str, meal_type: str, meal_button: WebElement):
        meal_data = {}

        day_of_week_header = self.driver.find_element(
            By.CSS_SELECTOR, f".flOORh:nth-child({day_of_week}) h2")
        meal_data["day_of_week"] = day_of_week_header.get_attribute(
            "innerText")

        meal_button.click()
        # Need to wait for meal data to load
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.ModalProductDescriptionContent")))

        meal_data["title"] = meal_button.accessible_name

        description = self.driver.find_element(
            By.CSS_SELECTOR, "div.ModalProductDescriptionContent")
        meal_data["description"] = description.get_attribute("innerText")

        meal_data["type"] = meal_type

        meal_data["section"] = section

        serving_size_element = self.driver.find_element(
            By.CSS_SELECTOR, "div.ModalProductServingSize")
        # Get rid of "Serving Size " in the text
        meal_data["serving_size"] = serving_size_element.get_attribute("innerText")[
            13:]

        calories_span = self.driver.find_element(
            By.CSS_SELECTOR, "li.Calories > span")
        meal_data["calories"] = int(calories_span.get_attribute("innerText"))

        calories_from_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Calories.From.Fat > span")
        calories_from_fat_text = calories_from_fat_span.get_attribute(
            "innerText")
        if calories_from_fat_text.isdigit():
            meal_data["calories_from_fat"] = int(calories_from_fat_text)
        else:
            meal_data["calories_from_fat"] = 0

        total_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Total.Fat > span")
        meal_data["total_fat"] = total_fat_span.get_attribute("innerText")

        saturated_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Saturated.Fat span.SpanNutrition")
        meal_data["saturated_fat"] = saturated_fat_span.get_attribute(
            "innerText")

        trans_fat_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Trans.Fat span.SpanNutrition")
        meal_data["saturated_fat"] = saturated_fat_span.get_attribute(
            "innerText")

        cholesterol_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Cholesterol span")
        meal_data["cholesterol"] = cholesterol_span.get_attribute("innerText")

        sodium_span = self.driver.find_element(By.CSS_SELECTOR, ".Sodium span")
        meal_data["sodium"] = sodium_span.get_attribute("innerText")

        total_carbs_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Total.Carbohydrates span")
        meal_data["total_carbohydrates"] = total_carbs_span.get_attribute(
            "innerText")

        dietary_fiber_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Dietary.Fiber span")
        meal_data["dietary_fiber"] = dietary_fiber_span.get_attribute(
            "innerText")

        sugar_span = self.driver.find_element(By.CSS_SELECTOR, ".Sugars span")
        meal_data["sugar"] = sugar_span.get_attribute("innerText")

        protein_span = self.driver.find_element(
            By.CSS_SELECTOR, ".Protein > span")
        meal_data["protein"] = protein_span.get_attribute("innerText")

        close_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[aria-label=\"Close\"]")
        close_button.click()

        return meal_data

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
        # self.change_meals(2)

        self.show_all()
        # self.get_meal_buttons(1)

        meals = []
        num_days = self.get_num_days()

        for i in range(1, num_days+1):
            meal_buttons = self.get_meal_buttons(i)

            for section_title in meal_buttons.keys():
                section_meal_buttons = meal_buttons[section_title]
                for button in section_meal_buttons:
                    meal_data = self.get_meal_data(
                        i, section_title, meal_type, button)
                    meals.append(meal_data)
        
        self.insert_into_db(meals)
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

    def insert_into_db(self, meal_data: List[Dict[str, Dict]]):
        date_strs = self.get_week_dates()
        database = HooEatsDatabase()
        for meal in meal_data:
            meal_date = date_strs[meal["day_of_week"]]
            uva_meals_query = "INSERT INTO uva_meals (title, dining_hall, meal_type, meal_date, meal_description, section, serving_size, calories, calories_from_fat, total_fat, saturated_fat, sugar, protein, dietary_fiber, total_carbohydrates, sodium) VALUES ('{title}', '{dining_hall}', '{meal_type}', '{meal_date}', '{meal_description}', '{section}', '{serving_size}', {calories}, {calories_from_fat}, '{total_fat}', '{saturated_fat}', '{sugar}', '{protein}', '{dietary_fiber}', '{total_carbohydrates}', '{sodium}');".format(
                title=meal["title"], dining_hall=self.dining_hall, meal_type=meal["type"], meal_date=meal_date, meal_description=meal["description"], section=meal["section"], serving_size=meal["serving_size"], calories=meal["calories"], calories_from_fat=meal["calories_from_fat"], total_fat=meal["total_fat"], saturated_fat=meal["saturated_fat"], sugar=meal["sugar"], protein=meal["protein"], dietary_fiber=meal["dietary_fiber"], total_carbohydrates=meal["total_carbohydrates"], sodium=meal["sodium"])
            database.execute(uva_meals_query, expect_results=False)
        database.close()


def main():
    url = "https://virginia.campusdish.com/LocationsAndMenus/ObservatoryHillDiningRoom"
    # url = "https://virginia.campusdish.com/en/locationsandmenus/freshfoodcompany/"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)
    chrome_driver = Service("../chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_driver, options=chrome_options)
    parser = CampusDishParser(driver, "Observatory Hill")
    print(parser.parse_menu())
    # print(parser.get_week_dates())


if __name__ == "__main__":
    main()
