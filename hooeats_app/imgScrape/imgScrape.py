import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
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
    imgURL_df = pd.DataFrame(columns = ["imageURL", "recipe_title"])
    df_100 = df.iloc[:100]
    #print(df.iloc[0].values[0])
    #print(df_50)
    #print(df_15_1)
    print(df_100)
    for i in range(101):
        try:
            imgURL_df = imgURL_df.append({'imageURL': recipe_images(df_100.iloc[i].values[0]), 'recipe_title': df_100.iloc[i].values[0]}, ignore_index = True)
        except:
            time.sleep(15)
            continue

    #for i in range(50):
     #   if i != 0:
      #      if i % 5 == 0:
       #         time.sleep(15)
        #        imgURL_df = imgURL_df.append({'imageURL': recipe_images(df_50.iloc[i].values[0])}, ignore_index = True)
         #   else:
          #      time.sleep(8)
           #     imgURL_df = imgURL_df.append({'imageURL': recipe_images(df_50.iloc[i].values[0])}, ignore_index = True)

    #for i in range(2500):
        #imgURL_df = imgURL_df.append({'imageURL': recipe_images(df.iloc[i].values[0])}, ignore_index = True)
        
    #imgURL_df = imgURL_df.append({'imageURL': recipe_images(df.iloc[3].values[0])}, ignore_index = True)
    #print(df.iloc[3].values[0])
    #print(recipe_images(df.iloc[3].values[0]))
    #print(imgURL_df)
    #print(imgURL_df.iloc[14].values[0])
    #print(imgURL_df.iloc[14].values[1])
    #print(df)
    #print(df.iloc[:,0])
    #print(combined_df)
    #print(combined_df.apply(recipe_images))
    #print(recipe_images("best banana bread 2886"))
    #print(recipe_images("creamy chocolate squares lite 57454"))
    #print(df.iloc[1])
    #df['imageURL'] = df.iloc[0].apply(recipe_images)
    #print(df)


    #df['imageURL'] = df.apply(lambda x : recipe_images(x['recipe_title']), axis = 1)

if __name__ == "__main__":
    main()