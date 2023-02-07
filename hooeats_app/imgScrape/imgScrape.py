import requests
from bs4 import BeautifulSoup

def recipe_images(recipe_title):

    recipe_title = recipe_title.replace(" ", "-")
    url = f"https://www.food.com/recipe/{recipe_title}"
    page = requests.get(url)
    parser = BeautifulSoup(page.content, "html.parser")

    #find div with class "primary-image"
    div = str(parser.find("div", class_="primary-image"))
    
    #I will change the naming of each variables later on
    begin = div.find("srcset") + 8
    first = div[begin:]
    end = first.find(".jpg") + 4
    final = first[:end]
    return final

def main():
    print(recipe_images("best banana bread 2886"))

if __name__ == "__main__":
    main()