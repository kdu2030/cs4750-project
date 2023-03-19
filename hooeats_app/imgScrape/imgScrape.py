import requests
from bs4 import BeautifulSoup
import pandas as pd
#from IPython.display import display

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
    data_import = pd.read_csv('recipes2500.csv', usecols = [0, 1])
    df = pd.DataFrame(data_import, columns=['name', 'id'])
    #print(df)
    #index_name = df[df['id'] == 86744].index
    #df.drop(index_name, inplace = True)
    df['recipe_title'] = df['name'] + " " + df['id'].astype(str)
    df = df.drop(['name', 'id'], axis=1)
    #print(df)
    #print(df.iloc[:,0])
    #print(combined_df)
    #print(combined_df.apply(recipe_images))
    #print(recipe_images("best banana bread 2886"))
    df['imageURL'] = df.apply(lambda row : recipe_images(row['recipe_title']), axis = 1)

if __name__ == "__main__":
    main()