import requests
from bs4 import BeautifulSoup

def recipe_images(recipe_title):

    print("1")
    recipe_title = recipe_title.replace(" ", "-")
    url = f"https://www.foods.com/recipe/{recipe_title}"
    print("2")
    page = requests.get(url)
    print("3")
    parser = BeautifulSoup(page.content, "html.parser")

    print("4")
    #find div with class "primary-image"
    div = parser.find("div", class_="primary-image")

    print("5")
    #image
    image = div.get("srcset").split(",")[0].strip().split(" ")[0]

    print("6")
    return image

def main():
    print("0")
    recipe_images("15 bean soup 51803")

if __name__ == "__main__":
    main()