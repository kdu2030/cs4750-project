import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from selenium.webdriver.common.by import By

class CampusDishParser:
    
    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url

    def change_to_weekly(self):
        change_weekly_button = self.driver.find_element(By.CSS_SELECTOR, ".DateMealFilterButton")
        change_weekly_button.click()
        weekly_option = self.driver.find_element(By.CSS_SELECTOR, "button.ButtonOutline")
        weekly_option.click()
        done_button = self.driver.find_element(By.CSS_SELECTOR, "button.Done")
        done_button.click()

    def change_meals(self, index: int = 0):
        change_meal_button = self.driver.find_element(By.CSS_SELECTOR, ".DateMealFilterButton")
        change_meal_button.click()
        meal_dropdown = self.driver.find_element(By.CSS_SELECTOR, ".css-1t70p0u-control")
        meal_dropdown.click()
        meal_option = self.driver.find_element(By.CSS_SELECTOR, f".css-wuv0vk > #react-select-2-option-{index}")
        meal_option.click()
        done_button = self.driver.find_element(By.CSS_SELECTOR, "button.Done")
        done_button.click()
        
    def get_meal_buttons(self, day_of_week:int) -> List[WebElement]:
        return self.driver.find_elements(By.CSS_SELECTOR, f".sc-ktCSKO > .nmzKf:nth-child({day_of_week}) button.HeaderItemNameLinkWeeklyMenu")
    
    def get_meal_data(self, day_of_week: int, meal_button: WebElement):
        meal_button.click()
        #Need to wait for meal data to load
        time.sleep(2)
        meal_data = {}

        title = self.driver.find_element(By.CSS_SELECTOR, "h2.ModalHeaderItemName")
        meal_data["title"] = title.get_attribute("innerText")

        day_of_week_header =  self.driver.find_element(By.CSS_SELECTOR, f".sc-ktCSKO > .nmzKf:nth-child({day_of_week}) > h2.gHIlKF")
        meal_data["day_of_week"] = day_of_week_header.get_attribute("innerText")
        
        serving_size_element = self.driver.find_element(By.CSS_SELECTOR, "div.ModalProductServingSize")
        #Get rid of "Serving Size " in the text
        meal_data["serving_size"] = serving_size_element.get_attribute("innerText")[13:]
        
        calories_span = self.driver.find_element(By.CSS_SELECTOR, "li.Calories > span")
        meal_data["calories"] = int(calories_span.get_attribute("innerText"))

        calories_from_fat_span = self.driver.find_element(By.CSS_SELECTOR, ".Calories.From.Fat > span")
        meal_data["calories_from_fat"] = calories_from_fat_span.get_attribute("innerText")

        total_fat_span = self.driver.find_element(By.CSS_SELECTOR, ".Total.Fat > span")
        meal_data["total_fat"] = total_fat_span.get_attribute("innerText")

        saturated_fat_span = self.driver.find_element(By.CSS_SELECTOR, ".Saturated.Fat span.SpanNutrition")
        meal_data["saturated_fat"] = saturated_fat_span.get_attribute("innerText")

        trans_fat_span = self.driver.find_element(By.CSS_SELECTOR, ".Trans.Fat span.SpanNutrition")
        meal_data["saturated_fat"] = saturated_fat_span.get_attribute("innerText")

        cholesterol_span = self.driver.find_element(By.CSS_SELECTOR, ".Cholesterol span")
        meal_data["cholesterol"] = cholesterol_span.get_attribute("innerText")

        sodium_span = self.driver.find_element(By.CSS_SELECTOR, ".Sodium span")
        meal_data["sodium"] = cholesterol_span.get_attribute("innerText")

        total_carbs_span = self.driver.find_element(By.CSS_SELECTOR, ".Total.Carbohydrates span")
        meal_data["total_carbohydrates"] = total_carbs_span.get_attribute("innerText")

        dietary_fiber_span = self.driver.find_element(By.CSS_SELECTOR, ".Dietary.Fiber span")
        meal_data["dietary_fiber"] = dietary_fiber_span.get_attribute("innerText")

        sugar_span = self.driver.find_element(By.CSS_SELECTOR, ".Sugars span")
        meal_data["sugar"] = sugar_span.get_attribute("innerText")

        protein_span = self.driver.find_element(By.CSS_SELECTOR, ".Protein > span")
        meal_data["protein"] = protein_span.get_attribute("innerText")

        close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Close\"]")
        close_button.click()

        return meal_data
        
        

    def add_cookies(self):
        date = datetime.now()
        # Get rid of mailing list promotion
        self.driver.add_cookie({"name": "IsShownMailSubscriptionWidget", "value":""})
        # Get rid of asking for cookies
        self.driver.add_cookie({"name": "OptanonConsent", "value": ""})
        self.driver.add_cookie({"name": "OptanonAlertBoxClosed", "value": date.strftime("%Y-%m-%dT%H:%M:%S")})
        self.driver.refresh()
    
    def get_all_meals(self):
        self.driver.get(self.url)
        self.add_cookies()
        self.change_to_weekly()

        # Need to wait for meal data to load
        time.sleep(15)
        #self.change_meals(2)
        
        meals = []
        meal_buttons = self.get_meal_buttons(1)


        
        
        for meal_button in meal_buttons:
            if len(meal_button.accessible_name) == 0:
                continue
            meal_data = self.get_meal_data(1, meal_button)
            meals.append(meal_data)
        
        print(meals)


def main():
    url = "https://virginia.campusdish.com/LocationsAndMenus/ObservatoryHillDiningRoom"
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_driver = Service("../chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_driver, options=chrome_options)
    driver.get(url)
    parser = CampusDishParser(driver, url)
    parser.get_all_meals()
    

if __name__ == "__main__":
    main()