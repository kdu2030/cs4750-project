from datetime import datetime, timedelta
from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.by import By
import string


class Runk:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://harvesttableuva.com/locations/runk-dining-hall/"

    def get_week_dates(self) -> List[str]:
        today = datetime.now()
        start_of_week = today - timedelta(days=((today.weekday()+1)))
        date_strs = []
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            date_strs.append(date.strftime("%Y-%m-%d"))
        return date_strs
        
    def get_meal_types(self) -> List[str]:
        meal_type_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".c-tabs-nav__link-inner")
        meal_types = []
        for meal_type_button in meal_type_buttons:
            meal_type_text = meal_type_button.get_attribute("innerText")
            parenthesis = meal_type_text.find(" (")
            if parenthesis != -1:
                meal_type_text = meal_type_text[:parenthesis]
            meal_types.append(string.capwords(meal_type_text))
        return meal_types
    
    def get_meal_links(self) -> Dict[str, List[WebElement]]:
        num_stations = len(self.driver.find_elements(By.CSS_SELECTOR, ".is-active .menu-station"))
        meal_links = {}
        for i in range(1, num_stations):
            title_element = self.driver.find_element(By.CSS_SELECTOR, f".is-active .menu-station:nth-child({i}) h4")
            meal_links[string.capwords(title_element.get_attribute("innerText"))] = self.driver.find_elements(By.CSS_SELECTOR, f".is-active .menu-station:nth-child({i}) a.show-nutrition")
        return meal_links
    
    def change_active_meal(self, index: int):
        meal_type_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".c-tabs-nav__link-inner")
        meal_type_buttons[index].click()
    
    
    def get_meal_data(self, station_title: str, date_str: str, meal_type: str, meal_link: WebElement):
        meal_data = {}
        print(meal_link.get_attribute("innerText"))
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(meal_link))
        meal_link.click()

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > h2")))

        meal_data["title"] = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > h2").get_attribute("innerText")

        try:
            description = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > p:nth-child(2)").get_attribute("innerText")
            meal_data["description"] = description
        except:
            meal_data["description"] = ""
            
        meal_data["type"] = meal_type

        meal_data["section"] = station_title

        meal_data["day_of_the_week"] = days_of_week[datetime.strptime(date_str, "%Y-%m-%d").weekday()]

        serving_size = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > thead > tr > th").get_attribute("innerText")
        meal_data["serving_size"] = serving_size.replace("Amount Per Serving", "").strip()

        calories = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(1) > th").get_attribute("innerText")
        meal_data["calories"] = int(calories.replace("Calories", "").replace(" ", ""))

        calories_from_fat = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(2) > th").get_attribute("innerText")
        meal_data["calories_from_fat"] = int(calories_from_fat.replace("Calories from Fat", " ").strip())

        total_fat = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(3) > th").get_attribute("innerText")
        meal_data["total_fat"] = total_fat.replace("Total Fat", "").strip()

        saturated_fat = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(4) > th").get_attribute("innerText")
        meal_data["saturated_fat"] = saturated_fat.replace("Saturated Fat", "").strip()

        trans_fat = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(5) > th").get_attribute("innerText")
        meal_data["trans_fat"] = trans_fat.replace("Trans Fat", "").strip()

        cholestorol = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(6) > th").get_attribute("innerText")
        meal_data["cholesterol"] = cholestorol.replace("Cholesterol", "").strip()

        sodium = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(7) > th").get_attribute("innerText")
        meal_data["sodium"] = sodium.replace("Sodium", "").strip()

        total_carbohydrates = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(8) > th").get_attribute("innerText")
        meal_data["total_carbohydrates"] = total_carbohydrates.replace("Total Carbohydrate", "").strip()

        dietary_fiber = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(9) > th").get_attribute("innerText")
        meal_data["dietary_fiber"] = dietary_fiber.replace("Dietary Fiber", "").strip()

        sugar = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(10) > th").get_attribute("innerText")
        meal_data["sugar"] = sugar.replace("Sugar", "").strip()

        protein = self.driver.find_element(By.CSS_SELECTOR, "#nutrition-slider-stage > div > div > table > tbody > tr:nth-child(11) > th").get_attribute("innerText")
        meal_data["protein"] = protein.replace("Protein", "").strip()

        close_button = self.driver.find_element(By.CSS_SELECTOR, ".close-nutrition")
        close_button.click()
        return meal_data
    
    def get_meal_type_data(self, meal_links: Dict[str, List[WebElement]], date_str: str, meal_type: str) -> List[Dict]:
        meal_type_data = []
        for station in meal_links.keys():
            for meal_link in meal_links[station]:
                meal_type_data.append(self.get_meal_data(station, date_str, meal_type, meal_link))
        return meal_type_data


    
    def get_all_meals(self):
        # self.driver.maximize_window()
        dates = self.get_week_dates()
        self.driver.get(self.base_url)
        meal_types = self.get_meal_types()
        meal_links = self.get_meal_links()
        self.change_active_meal(0)
        print(self.get_meal_type_data(meal_links, dates[0], meal_types[0]))

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_driver = Service("../chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_driver, options=chrome_options)
    runk_parser = Runk(driver)
    runk_parser.get_all_meals()

if __name__ == "__main__":
    main()