from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from selenium.webdriver.common.by import By

class CampusDishParser:
    
    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url


    def change_meals(self, index: int = 0):
        change_meal_button = self.driver.find_element(By.CSS_SELECTOR, ".DateMealFilterButton")
        change_meal_button.click()
        meal_dropdown = self.driver.find_element(By.CSS_SELECTOR, ".css-1t70p0u-control")
        meal_dropdown.click()
        meal_option = self.driver.find_element(By.CSS_SELECTOR, f".css-wuv0vk > #react-select-2-option-{index}")
        meal_option.click()
        done_button = self.driver.find_element(By.CSS_SELECTOR, "button.Done")
        done_button.click()

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
        self.change_meals(2)


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